#!/bin/bash

light_par=$(if [ $@ -gt 0 ]; then echo 'A'; else echo 'U'; fi)
amount=$(echo $@ | grep -o -E '[[:digit:]]+')
light -$light_par $amount

cur_bright=$(light | grep -o -E '[[:digit:]]+' | head -n 1)

icon='display-brightness-off'
if [ $cur_bright -gt 70 ]; then
    icon='display-brightness-high'
elif [ $cur_bright -gt 40 ]; then
    icon='display-brightness-medium'
elif [ $cur_bright -gt 0 ]; then
    icon='display-brightness-low'
fi

notify-send.py brightness --replaces-process brightness_ctl -i $icon --hint int:value:$cur_bright
