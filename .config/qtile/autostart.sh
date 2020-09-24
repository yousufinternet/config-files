#!/bin/sh
localectl --no-convert set-x11-keymap us,ara pc104 ,qwerty 'grp:alt_shift_toggle,caps:swapescape' &
setxkbmap -option "caps:escape" -option "altwin:menu_win" -option "terminate:ctrl_alt_bksp" &
picom &
~/.config/bspwm/scripts/set_wallpaper.py &
redshift &
sxhkd -c ~/.config/sxhkd/apps_keys &
systemctl --user start xfce4-notifyd &
~/.config/bspwm/bar/start_bar_i3.py &
xfce4-panel -d &
mpd &
nm-applet &
udiskie -t &
blueman-applet &
pasystray &
parcellite &
emacs --daemon &
# exec ~/Documents/sshfs-watchdog/sshfs-wd.sh &
perWindowLayoutD &
