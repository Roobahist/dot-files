# Portable macOS dotfiles

Public, machine-independent configuration for AeroSpace, Alacritty, Atuin, Karabiner-Elements, SketchyBar, and a wallpaper color helper.

This repository is the source of truth for portable configuration used by [mac-setup](https://github.com/Roobahist/mac-setup). It contains no account credentials, shell history, machine-specific exports, or private workflow automations.

## Install

Requires macOS. Clone into a directory you control, then create links into your `~/.config` directory:

```sh
git clone https://github.com/Roobahist/dot-files.git ~/dot-files
cd ~/dot-files
bash install.sh
```

`install.sh` preserves conflicting existing configuration outside the repository before creating links. Review its changes before running it. It does not install the applications themselves.

## Update

```sh
cd ~/dot-files
git pull --ff-only
bash apply.sh
```

The links point to files in the clone, so most changes are visible to applications as soon as the pull completes. Some apps require a reload or new session.

## Layout

- `aerospace/`: window-manager configuration
- `alacritty/`: terminal configuration and theme
- `atuin/`: history-tool preferences, not history data
- `karabiner/`: keyboard configuration and app-launch scripts
- `sketchybar/`: bar configuration and plugins
- `unsplash/`: local wallpaper accent helper

## Portable paths and custom mappings

All shell-command paths in Karabiner resolve from `$HOME` at runtime, rather than referencing one macOS username. One generic, disabled example demonstrates mapping a single key to a sequence of keys. Enable or adapt it explicitly if desired.

## Privacy

Only deliberately selected configuration files belong here. Do not commit application databases, authentication material, environment secrets, logs, exports, or personal information. `.gitignore` reduces accidental commits but is not a security boundary; review diffs before each push.

This repository begins with a clean, independent history. The original private dotfiles repository and its history are not copied into this public repository.

## Relationship to mac-setup

`mac-setup` bundles versioned snapshots of the portable files from this repository so its releases can run without GitHub access. Changes here trigger a synchronization pull request in `mac-setup` when the optional dispatch secret is configured; a scheduled check is the fallback. `mac-setup`'s Vorssaint profile remains separate.

Do not use the `mac-setup` profile installer to overwrite a configuration directory you are intentionally maintaining as a symlink to this checkout. Manage that linked configuration with `git pull` and `apply.sh` instead.

## Reference behavior and portability

The AI workspace uses the runtime ID `ai` consistently in persistent workspaces,
keyboard destinations, app routing and SketchyBar. Older personal configurations
may call the same workspace `chatgpt`. The app migrates that known legacy identity.

Karabiner retains separate Chrome, Alacritty, Visual Studio Code, Finder and Telegram rules.
Active rules match the local reference after replacing personal script paths with
quoted `$HOME` paths. Private disabled automations are excluded; the generic disabled
example is public documentation. Chrome profile numbers are local slot numbers; no
Chrome account names or profile databases are shared. SF Pro workspace symbols use
SF Pro; numbers use Hack Nerd Font. Install both fonts before testing the bar.

Telegram is routed to Messages, whose default destination shortcut is Option+0.
Option+T opens or focuses Telegram through its separate Karabiner rule. This binding
was previously managed by Raycast; remove that Raycast app hotkey when migrating
an existing machine so Karabiner is the sole owner. No Raycast databases are exported.
