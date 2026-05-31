# LockBox Handoff

## Current Project Status
v0.1.0 - CLI complete. TUI redesigned twice - v2 fixes contrast/button rendering issues seen in screenshot.

## Completed Features
- `lockbox init`, add, get, list, update, delete, generate, changemaster, docs
- `lockbox ui` - full Textual TUI (v2 redesign, high contrast)

## TUI Design (v2)
Aesthetic: GitHub dark / Claude Code inspired
Palette (hardcoded hex, not CSS vars - more reliable in Textual):
- `#0d1117`  bg (near black)
- `#161b22`  surface (panels, sidebar, topbar)
- `#21262d`  elevated surface (card borders, hover states)
- `#30363d`  border default
- `#388bfd`  border focus / accent hi
- `#58a6ff`  accent (titles, selected items)
- `#c9d1d9`  text primary
- `#8b949e`  text dim (labels, hints)
- `#484f58`  text muted (card field keys, status bar)
- `#1f6feb`  button primary bg
- `#3fb950`  green (success)
- `#f85149`  red (danger/error)

Key CSS decisions:
- All CSS in single APP_CSS string at module level, shared across all classes via CSS = APP_CSS
- Button base reset overrides Textual defaults globally (border: tall, not round - more visible)
- `border: tall` for interactive elements (taller hit border), `border: solid` for containers
- No `round` borders - `solid` and `tall` render more crisply at low terminal resolutions
- `-danger` class on Delete buttons for red styling
- Static used for topbar title/divider (no button chrome)

Layout:
- Topbar: 3 rows, surface bg, solid border-bottom
- Sidebar: 22 cols, service list with [n] count badges
- Detail pane: scrollable EntryCard widgets
- Status bar: 1 row at bottom

## File Structure
```
LockBox/
  src/lockbox/
    __init__.py
    __main__.py
    cli.py          - typer + rich CLI
    vault.py        - encryption
    generator.py    - password generator
    tui.py          - Textual TUI (v2)
    docs.py         - inline doc strings
  pyproject.toml
  requirements.txt
  extra/handoff.md
```

## Known Issues
- pyperclip may fail on headless Linux; graceful fallback exists
- Old root-level main.py/vault.py/generator.py not deleted (no delete tool)
- get --copy-password with multiple entries copies only the first

## Pending Features
- `lockbox search <term>`
- `lockbox export` / `lockbox import`
- Notes field on entries
- PyInstaller .exe
- TUI keyboard nav through cards (tab/arrow keys)
- TUI Ctrl+C to copy from focused card

## Next Recommended Tasks
1. `lockbox ui` - verify buttons/borders render with proper contrast
2. Add `lockbox search` CLI command
3. PyInstaller build

## Implementation Notes
- camelCase throughout (no underscores unless Textual requires)
- No comments, no docstrings
- Textual CSS vars were unreliable across component boundaries; switched to hardcoded hex
- `border: tall` is a Textual-specific border style that renders as a visible 1-cell border
  suitable for buttons; prefer over `round` for legibility at normal terminal font sizes
