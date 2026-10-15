# macOS preferences

`preferences.json` is the source of truth for the portable macOS preferences shared with Mac Setup. It records selected settings from the reference Mac, including explicit system defaults (`null`), rather than exporting complete preference domains. App profiles, credentials, display geometry, privacy permissions and private application data are not part of this file.

macOS does not automatically read this file. Mac Setup reads it and applies changes through the macOS preferences subsystem. Install a current Mac Setup CLI or app first; no Python runtime or background agent is required.

```sh
bash macos/apply.sh plan
bash macos/apply.sh apply
bash macos/apply.sh off
bash macos/apply.sh on
```

`apply`, `on` and `off` show a plan and ask before writing. Add `--yes` for an already reviewed noninteractive run. `on` and `off` update the top-level `enabled` flag and reconcile the whole profile. You can also edit that flag directly and run `apply`. To manage a single setting, change its `enabled` or `value` and run `apply`. An enabled setting whose value is `false` writes false; a disabled setting releases management and restores its previous value. `null` removes the stored override and uses the system default. `minimumOS` skips unsupported settings.

Disabling settings or the whole profile restores the values saved before first management, rather than guessing opposite values. Later manual edits are kept and reported when releasing a setting. Repeated applies retain the original baseline. Removing a setting from the file releases it on the next full apply. Changes are journaled, verified and rolled back on failure; `mac-setup backups` and `mac-setup restore` expose recovery records. Backups can contain personal preferences and stay in `~/Library/Application Support/mac-setup`, outside Git.

Mac Setup uses `~/.config/macos/preferences.json` (or the XDG config directory); `install.sh` links this folder there. Without an installed file, the app uses its bundled snapshot and creates a local copy when you first apply a preference. Its Appearance page provides the whole-profile review and on/off control. Individual preference controls update the same file, so a later group apply respects your changes. Editing a linked profile changes the local dotfiles checkout; nothing automatically commits or pushes your customizations.

`bash apply.sh` applies this profile before reloading other application configs. `git pull` alone never applies system preferences. Some changes require logout or reopening apps. Finder/Dock/menu-bar processes are refreshed only when an affected stored value changes. Finish Finder file operations before applying. Manual permissions, UI-only appearance options and hardware-specific display choices remain manual; this profile does not attempt to bypass macOS approval.

`finder-list` stores only list-view options. Applying it merges those options into existing Finder view dictionaries while preserving column widths and unrelated settings. Nonempty pinned Dock tiles are intentionally not exported because they can include personal paths and URLs; the public profile only contains portable empty lists.
