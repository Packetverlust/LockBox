#!/usr/bin/env bash
set -e
pip install -e ".[dev]"
pip install argon2-cffi
pyinstaller \
  --onefile \
  --name lockbox-linux \
  --paths src \
  src/lockbox/__main__.py