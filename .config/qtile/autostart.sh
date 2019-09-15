#!/bin/sh
compton -f &
mpd &
systemctl --user start xfce4-notifyd &
safeeyes &
redshift &
goldendict &
nm-applet &
udiskie -t &
blueman-applet &
pasystray &
syncthing-gtk -m &
parcellite &
emacs --daemon &
kdeconnect-indicator &
~/.config/i3/dynamic_wallpaper.py &
XDG_CONFIG_HOME=~/.config_alt xfce4-panel -d &
# exec ~/Documents/sshfs-watchdog/sshfs-wd.sh &
localectl --no-convert set-x11-keymap us,ara pc104 ,qwerty 'grp:alt_shift_toggle,caps:swapescape' &
setxkbmap -option caps:escape &
