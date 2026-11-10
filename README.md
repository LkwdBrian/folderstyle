# FolderStyle - MacOS Folder Styles for Claude

A Claude skill that color-codes macOS folders and puts a symbol or emoji on them, so folders Claude creates or reorganizes for you are easy to scan in Finder.

It uses the folder customization introduced in macOS 26 Tahoe: a tint taken from a Finder tag color, plus an SF Symbol or emoji drawn on the folder icon.

## Requirements

- macOS 26 (Tahoe) or later for the folders you want to style
- Python 3 (the macOS Command Line Tools include it)
- A Claude setup that can run shell commands: Claude Code, or the Claude desktop app with a connected folder

## Install

Claude Code (personal skill):

```
git clone https://github.com/LkwdBrian/folderstyle ~/.claude/skills/folderstyle
```

Then ask Claude to create or organize some folders, or call the script yourself.

## Use the script directly

```
python3 scripts/folderstyle.py <folder> <Color|-> <sym:NAME|emoji:CHAR|->

python3 scripts/folderstyle.py ~/Documents/Taxes Orange sym:banknote.fill
python3 scripts/folderstyle.py ~/Documents/Trips - emoji:✈️
```

Colors: Gray, Green, Purple, Blue, Yellow, Red, Orange.

## How it works

Three extended attributes on the folder:

| Attribute | Purpose |
|---|---|
| `com.apple.metadata:_kMDItemUserTags` | Finder tag color, which also tints the folder |
| `com.apple.icon.folder#S` | JSON with `{"sym":"..."}` or `{"emoji":"..."}` |
| `com.apple.FinderInfo` | Custom-icon flag so symbol-only folders render |

## What testing found

- **No dots in folder names.** A folder called `notes.fill` is treated like a document type and the symbol never draws. Dots inside the symbol name are fine.
- **Symbols beyond Finder's picker work.** Any name in the system symbol catalog should render. Names outside it fail silently, with no error.
- **Verified names** are listed in `SKILL.md`.

## Caveats

- The attributes are undocumented and may change in a macOS update.
- Developed through a Linux shell bridge to a Mac folder, then confirmed running natively in macOS 26 Terminal (where it shells out to `xattr`). Please open an issue if it misbehaves on your setup.
- Custom icons show as generic folders in the Dock, and Finder aliases do not carry the customization.
- Not affiliated with Apple or Anthropic. SF Symbols belong to Apple, and this repo does not include them.

## Credits

- Sam Henri Gold, for finding that arbitrary SF Symbol names work through the xattr
- Howard Oakley (The Eclectic Light Company), for documenting how Tahoe stores folder customization
- The CC0 zsh script on MacScripter by QuickTimer, which showed the tag plist format

## License

MIT
