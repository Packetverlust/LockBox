pip install -e ".[dev]"
pip install argon2-cffi
pyinstaller `
  --onefile `
  --name lockbox `
  --paths src `
  src/lockbox/__main__.py