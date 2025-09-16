#!/usr/bin/env bash

# Install Niri's dependencies
paru -S --needed niri-git \
    hypridle \
    xdg-desktop-portal-gtk \
    xdg-desktop-portal-gnome \
    nautilus \
    gnome-keyring \
    polkit-kde-agent \
    xwayland-satellite \
    lm_sensors

# Install Dank Material Shell
paru -S --needed \
    dms-shell-git \
    cava wl-clipboard cliphist brightnessctl \
    matugen-bin dgop

# Enable Niri's services
systemctl --user add-wants niri.service hypridle.service
systemctl --user add-wants niri.service gnome-polkit.service
systemctl --user add-wants niri.service syncthingtray.service
