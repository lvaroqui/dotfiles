if status is-interactive
    # Commands to run in interactive sessions can go here
end

# Path configuration
set -gx PATH $HOME/.cargo/bin $PATH

# Rust configuration
set -gx RUSTC_WRAPPER $HOME/.cargo/bin/sccache

# atuin (command history manager) setup
atuin init --disable-up-arrow fish | source

# Tide prompt configuration
set -g tide_cmd_duration_threshold 0
set -g tide_cmd_duration_decimals 3

# Git shortcuts
function gst --description 'git status shortcut'
    git status $argv
end

function glg --description 'git log with graph'
    git log --oneline --graph --all --decorate $argv
end