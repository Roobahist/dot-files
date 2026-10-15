#!/usr/bin/env bash
# Use Mac Setup's native, journaled preference implementation.
set -euo pipefail
MACOS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$(command -v mac-setup || true)"
if [[ -z "$CLI" ]]; then
  for candidate in "/Applications/Mac Setup.app/Contents/MacOS/mac-setup" "$HOME/Applications/Mac Setup.app/Contents/MacOS/mac-setup"; do
    if [[ -x "$candidate" ]]; then CLI="$candidate"; break; fi
  done
fi
if [[ -z "$CLI" ]]; then
  echo "Install the current Mac Setup CLI or app first: https://github.com/Roobahist/mac-setup" >&2
  exit 1
fi
if [[ $# -eq 0 ]]; then set -- apply; fi
exec "$CLI" macos "$@" --config "$MACOS_DIR/preferences.json"
