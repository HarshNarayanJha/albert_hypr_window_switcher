# Albert Hyprland Window Switcher Plugin

Quickly search through and switch to open windows right from your favourite launcher in your favourite wm.

### Install

> [!NOTE]
> The latest version of this plugin (v4.0 or later) requires Hyprland v0.55.0 or later. This is because the syntax of dispatchers changed in that version to lua.
> Note that the plugin continues to function, only the actions will not function. We always target the latest tagged release of hyprland.

To install, copy or symlink this directory to `~/.local/share/albert/python/plugins/albert_hypr_window_switcher/`

Or just run `git clone https://github.com/HarshNarayanJha/albert_hypr_window_switcher ~/.local/share/albert/python/plugins/albert_hypr_window_switcher/`

### Development Setup

I use the Zed Editor (naturally). Python Development includes `pyright` as `lsp` and `ruff` as `linter`.

Copy the `albert.pyi` file from `~/.local/share/albert/python/plugins/albert.pyi` to this directory for type definitions and completions!

### References

- The official (now removed) window switcher - https://github.com/albertlauncher/python/blob/46696a2c196ccf7ecb34f82c33b585197facd29e/window_switcher.py
- Windows Switcher Plus - https://github.com/VietTralala/window-switcher-plus
- Hyprland (hyprctl) - hyprland.org
