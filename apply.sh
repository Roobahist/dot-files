#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$REPO_DIR/macos/apply.sh" apply "$@"

echo "Applying configs..."

if command -v aerospace >/dev/null 2>&1; then
  aerospace reload-config || true
fi

if command -v brew >/dev/null 2>&1; then
  if brew services list 2>/dev/null | grep -q '^sketchybar'; then
    brew services restart felixkratz/formulae/sketchybar || true
  fi
fi

echo "Karabiner watches its config automatically."
echo "Alacritty and Atuin will use updated config in new sessions/windows as applicable."
echo "Done."
