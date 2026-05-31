#!/usr/bin/env bash

set -e

REPO="packetverlust/lockbox"
INSTALL_DIR="$HOME/.local/bin"
BIN="$INSTALL_DIR/lockbox"

echo ""
echo "  LockBox Installer"
echo "  ─────────────────"
echo ""

echo "  Fetching latest release..."
RELEASE=$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest")
VERSION=$(echo "$RELEASE" | grep '"tag_name"' | cut -d'"' -f4)
DOWNLOAD_URL=$(echo "$RELEASE" | grep '"browser_download_url"' | grep -i linux | cut -d'"' -f4 | head -1)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "  [ERROR] No Linux binary found in release $VERSION"
    exit 1
fi

echo "  Latest version: $VERSION"

mkdir -p "$INSTALL_DIR"

TMP=$(mktemp)
echo "  Downloading..."
curl -fsSL "$DOWNLOAD_URL" -o "$TMP"
chmod +x "$TMP"
mv "$TMP" "$BIN"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "  Add this to your ~/.bashrc or ~/.zshrc:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "  LockBox $VERSION installed to $BIN"
echo "  Run: lockbox --help"
echo ""
