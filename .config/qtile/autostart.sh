#!/bin/sh
compton -f --inactive-dim 0.1 -c --backend glx &
mpd &
systemctl --user start xfce4-notifyd &
exec ~/.config/i3/dynamic_wallpaper.py &
safeeyes &
redshift &
goldendict &
nm-applet &
udiskie -t &
blueman-applet &
pasystray &
syncthing-gtk -m &
parcellite &
exec ~/Documents/sshfs-watchdog/sshfs-wd.sh &
localectl --no-convert set-x11-keymap us,ara pc104 ,qwerty 'grp:alt_shift_toggle,caps:swapescape' &
setxkbmap -option caps:escape &
