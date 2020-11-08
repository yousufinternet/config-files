#!/bin/bash

pactl set-sink-volume @DEFAULT_SINK@ $@%

cur_vol=$(pamixer --get-volume)

icon='notification-audio-volume-muted'
if [ $cur_vol -gt 70 ]; then
    icon='notification-audio-volume-high'
elif [ $cur_vol -gt 40 ]; then
    icon='notification-audio-volume-medium'
elif [ $cur_vol -gt 0 ]; then
    icon='notification-audio-volume-low'
fi

#notify-send.py volume --replaces-process volume_ctl -i $icon --hint int:value:$cur_vol
dunstify --replace=001 --icon=$icon --hints=int:value:$cur_vol --appname=Volume ""
