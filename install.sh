#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$HOME/.dotfiles-install-backup-$TIMESTAMP"

MANAGED=(
  aerospace
  alacritty
  atuin
  karabiner
  sketchybar
  unsplash
)

mkdir -p "$CONFIG_DIR" "$BACKUP_DIR"

echo "Repository: $REPO_DIR"
echo "Backup:     $BACKUP_DIR"
echo

for name in "${MANAGED[@]}"; do
  repo_path="$REPO_DIR/$name"
  target_path="$CONFIG_DIR/$name"

  if [ ! -d "$repo_path" ]; then
    echo "Skipping $name: repository directory does not exist yet."
    continue
  fi

  if [ -L "$target_path" ]; then
    current_target="$(readlink "$target_path")"
    if [ "$current_target" = "$repo_path" ]; then
      echo "$name: already linked"
      continue
    fi

    mv "$target_path" "$BACKUP_DIR/$name.symlink"
  elif [ -e "$target_path" ]; then
    mv "$target_path" "$BACKUP_DIR/$name"
  fi

  ln -s "$repo_path" "$target_path"
  echo "$name: linked"
done

echo
echo "Installation complete."
echo "Any replaced local configuration was moved to:"
echo "  $BACKUP_DIR"
