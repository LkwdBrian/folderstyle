---
name: folderstyle
description: Set a Finder tint (tag color) and an SF Symbol or emoji on macOS Tahoe folders. Use when creating or reorganizing folders on a Mac and the user wants them color-coded and labeled with symbols.
---

# FolderStyle - MacOS Folder Styles for Claude

Applies the macOS 26 (Tahoe) folder look: a tint from a Finder tag color plus a symbol or emoji drawn on the folder icon. Style every new folder you create. Restyle existing folders only when asked.

## Usage

```
python3 -I scripts/folderstyle.py <folder> <Color|-> <sym:NAME|emoji:CHAR|->
```

Examples:

```
python3 -I scripts/folderstyle.py ~/Documents/Taxes Orange sym:banknote.fill
python3 -I scripts/folderstyle.py ~/Documents/Trips - emoji:✈️
python3 -I scripts/folderstyle.py ~/Documents/Archive Gray -
```

Colors: Gray, Green, Purple, Blue, Yellow, Red, Orange. Use `-` to skip the color or the glyph. The script prints the attributes it wrote.

The script runs natively on macOS and from a Linux shell that has a Mac folder mounted (for example a desktop-app bridge). Pass paths as arguments and run Python with `-I`.

## How it works

- Tint and label: a Finder tag color in `com.apple.metadata:_kMDItemUserTags`, written as a binary plist of strings like `Orange\n7`.
- Symbol: `com.apple.icon.folder#S` holding `{"sym":"house.fill"}` or `{"emoji":"🏠"}`.
- `com.apple.FinderInfo` gets the custom-icon flag (byte 8, 0x04) so a symbol-only folder renders.
- All three are undocumented. Verify after writing and report failures plainly.

## Rules learned in testing

1. Never put a `.` in the name of a folder you style. Names like `v2.0` or `notes.fill` look like a document type to Finder and the symbol silently does not render. Use dashes. If a dotted folder exists, offer to rename it with `mv`; the attributes travel with it.
2. Dots inside the symbol name are fine (`house.fill`).
3. A symbol name that is not in the system catalog fails silently with a plain folder. Ask the user to check any new name in Finder before relying on it.
4. Many symbols outside Finder's Customize Folder picker work, including recent ones.
5. Skip system folders (Applications, Library, System, Users) and anything outside folders the user gave you.
6. Existing non-color tags are kept. An existing standard color tag is replaced.
7. Requires macOS 26 or later. Say so and skip on older systems.

## Verified symbols (rendered in Finder on macOS 26)

house.fill, banknote.fill, building.columns.fill, person.2.fill, airplane, antenna.radiowaves.left.and.right, camera.fill, cross.case.fill, star.fill, atom, hurricane, scissors, stethoscope, tortoise.fill, cup.and.saucer.fill, teddybear.fill, bolt.horizontal.fill, dice.fill, sailboat.fill, puzzlepiece.extension.fill, applescript.fill, externaldrive.connected.to.line.below.fill, textformat.characters.arrow.left.and.right, dollarsign.gauge.chart.leftthird.topthird.rightthird. Emoji also work.

Known to fail: names that are not in the catalog.

## Color scheme

Ask the user for their scheme, or edit this default:

| Color | Meaning |
|---|---|
| Blue | Work |
| Green | Home and property |
| Purple | Business or side projects |
| Orange | Finance, legal, tax |
| Red | Urgent, needs action |
| Yellow | In progress, drafts |
| Gray | Archive, reference |

## Workflow

1. Create folders with dot-free names, then style them in the same step.
2. Report what you applied in a short table (folder, color, symbol).
3. If a symbol does not show, check the folder name for dots first, then try an emoji.
4. Mention any symbol not on the verified list so the user can confirm it in Finder.
