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
    for RC in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$RC" ] && ! grep -q ".local/bin" "$RC"; then
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC"
            echo "  Added to PATH in $RC"
        fi
    done

    FISH_CONFIG="$HOME/.config/fish/config.fish"
    mkdir -p "$(dirname "$FISH_CONFIG")"
    if ! grep -q ".local/bin" "$FISH_CONFIG" 2>/dev/null; then
        echo "set -gx PATH \$HOME/.local/bin \$PATH" >> "$FISH_CONFIG"
        echo "  Added to PATH in $FISH_CONFIG"
    fi

    export PATH="$INSTALL_DIR:$PATH"
fi

echo ""
echo "  LockBox $VERSION installed to $BIN"
echo "  Run: lockbox --help"
echo "  (If 'lockbox' is not found, restart your terminal)"
echo ""
