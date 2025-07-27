local wezterm = require 'wezterm'

local config = wezterm.config_builder()
local act = wezterm.action

config.color_scheme = 'Dracula'

config.enable_tab_bar = false

config.font = wezterm.font '0xProto Nerd Font Mono'

config.window_background_opacity = 0.8

config.window_padding = {
    left = 0,
    right = 0,
    top = 0,
    bottom = 0
}

config.keys = {{
    key = 'Backspace',
    mods = 'CTRL',
    action = act.SendKey {
        key = 'w',
        mods = 'CTRL'
    }
}}

config.scrollback_lines = 20000

config.window_decorations = "NONE"

return config
