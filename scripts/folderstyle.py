#!/usr/bin/env python3
"""FolderStyle: set a Finder tint (tag color) and a symbol/emoji on a folder (macOS 26 Tahoe+).

usage: folderstyle.py <folder> <Color|-> <sym:NAME|emoji:CHAR|->

Works natively on macOS (via the xattr tool) and from a Linux shell that has a
Mac folder mounted (via os.setxattr). Uses undocumented Finder attributes.
"""
import json
import os
import plistlib
import subprocess
import sys

COLORS = {"Gray": 1, "Green": 2, "Purple": 3, "Blue": 4,
          "Yellow": 5, "Red": 6, "Orange": 7}
TAGS = "com.apple.metadata:_kMDItemUserTags"
ICON = "com.apple.icon.folder#S"
FINDER_INFO = "com.apple.FinderInfo"


def get_attr(path, name):
    if sys.platform == "darwin":
        r = subprocess.run(["/usr/bin/xattr", "-px", name, path],
                           capture_output=True, text=True)
        return bytes.fromhex("".join(r.stdout.split())) if r.returncode == 0 else None
    try:
        return os.getxattr(path, name)
    except OSError:
        return None


def set_attr(path, name, data):
    if sys.platform == "darwin":
        subprocess.run(["/usr/bin/xattr", "-wx", name, data.hex(), path], check=True)
    else:
        os.setxattr(path, name, data)


def style(path, color, glyph):
    path = path.rstrip("/")
    if not os.path.isdir(path):
        sys.exit(f"not a folder: {path}")
    if "." in os.path.basename(path):
        sys.exit("folder name contains a dot; rename it first, "
                 "otherwise Finder will not draw the symbol")

    if color != "-":
        if color not in COLORS:
            sys.exit(f"color must be one of {', '.join(COLORS)}")
        raw = get_attr(path, TAGS)
        tags = plistlib.loads(raw) if raw else []
        # keep the user's other tags, replace any standard color tag
        tags = [t for t in tags if t.split("\n")[0] not in COLORS]
        tags.append(f"{color}\n{COLORS[color]}")
        set_attr(path, TAGS, plistlib.dumps(tags, fmt=plistlib.FMT_BINARY))

    if glyph != "-":
        kind, _, value = glyph.partition(":")
        if kind not in ("sym", "emoji") or not value:
            sys.exit("glyph must look like sym:house.fill or emoji:🏠")
        set_attr(path, ICON, json.dumps({kind: value}, ensure_ascii=False).encode())

    # custom-icon flag (byte 8, 0x04) so a symbol-only folder renders
    info = bytearray(get_attr(path, FINDER_INFO) or bytes(32))
    info[8] |= 0x04
    set_attr(path, FINDER_INFO, bytes(info))

    tags_raw = get_attr(path, TAGS)
    print(os.path.basename(path),
          "| tags:", plistlib.loads(tags_raw) if tags_raw else None,
          "| icon:", (get_attr(path, ICON) or b"").decode())


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    style(*sys.argv[1:4])
