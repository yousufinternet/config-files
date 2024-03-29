#!/bin/bash

light_par=$(if [ $@ -gt 0 ]; then echo 'inc'; else echo 'dec'; fi)
amount=$(echo $@ | grep -o -E '[[:digit:]]+')
xbacklight -$light_par $amount

# cur_bright=$(xbacklight -get | grep -o -E '[[:digit:]]+' | head -n 1)
cur_bright=$(xbacklight -get)

icon='notification-display-brightness-off'
if [ $cur_bright -gt 70 ]; then
    icon='notification-display-brightness-high'
elif [ $cur_bright -gt 40 ]; then
    icon='notification-display-brightness-medium'
elif [ $cur_bright -gt 0 ]; then
    icon='notification-display-brightness-low'
fi

#notify-send.py brightness --replaces-process brightness_ctl -i $icon --hint int:value:$cur_bright
dunstify --replace=002 --icon=$icon --hints=int:value:$cur_bright --appname=Brightness ""
