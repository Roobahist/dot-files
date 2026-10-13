#!/usr/bin/env bash

set -euo pipefail

TARGET="$HOME/.gitignore_global"
SOURCE_URL="https://raw.githubusercontent.com/github/gitignore/main/Global/macOS.gitignore"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required to download GitHub's official macOS gitignore template."
  exit 1
fi

echo "Downloading GitHub's official macOS global gitignore..."
curl -fsSL "$SOURCE_URL" -o "$TARGET"

git config --global core.excludesfile "$TARGET"

echo "Configured:"
echo "  core.excludesfile = $TARGET"
