#!/usr/bin/env bash

# Install Niri's dependencies
paru -S niri swayidle swaybg swaylock-effects waybar mako

# Enable Niri's services
systemctl --user add-wants niri.service mako.service
systemctl --user add-wants niri.service waybar.service
systemctl --user add-wants niri.service swayidle.service
systemctl --user add-wants niri.service swaybg.service
