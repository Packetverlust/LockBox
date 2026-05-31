# Building LockBox from Source

## Requirements

- Python 3.10 or newer
- pip

## Clone and install

```powershell
git clone https://github.com/yourname/lockbox.git
cd lockbox
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
```

On Linux / macOS:
```bash
source venv/bin/activate
pip install -e .
```

After this `lockbox` is available as a command in the active venv.

## Optional: TUI support

The TUI (`lockbox ui`) requires Textual:

```
pip install textual
```

## Optional: clipboard support on Linux

pyperclip needs xclip or xsel:

```bash
sudo apt install xclip
```

## Running directly without installing

```powershell
python -m lockbox
```

## Building a standalone .exe (Windows)

```powershell
pip install pyinstaller
pyinstaller --onefile --name lockbox src/lockbox/__main__.py
```

Output is in `dist/lockbox.exe`. Copy it anywhere on your PATH.

## Project layout

```
lockbox/
  src/lockbox/
    __init__.py      version string
    __main__.py      python -m lockbox entry point
    cli.py           all CLI commands (Typer + Rich)
    tui.py           interactive TUI (Textual)
    vault.py         encryption, key derivation, load/save
    generator.py     password generator
    docs.py          inline docs content
  docs/
    docs.md          this file
    setup.md         build instructions
  extra/
    handoff.md       developer handoff notes
  pyproject.toml
  requirements.txt
  README.md
```
