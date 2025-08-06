#!/usr/bin/env bash

# Install Niri's dependencies
paru -S niri \
    swayidle \
    swaybg \
    hyprlock \
    waybar \
    mako \
    xdg-desktop-portal-gtk \
    xdg-desktop-portal-gnome \
    nautilus \
    gnome-keyring \
    polkit-kde-agent \
    xwayland-satellite \
    lm_sensors

# Enable Niri's services
systemctl --user add-wants niri.service mako.service
systemctl --user add-wants niri.service waybar.service
systemctl --user add-wants niri.service swayidle.service
systemctl --user add-wants niri.service swaybg.service
