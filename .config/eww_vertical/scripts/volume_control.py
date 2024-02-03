#!/usr/bin/env python
import sys
import subprocess as sp

icons = {0: '\uf026', 35: '\uf027', 100: '\uf028'}
actions = {
        'max': 'pactl set-sink-volume @DEFAULT_SINK@ 100%',
        'mute': 'pactl set-sink-volume @DEFAULT_SINK@ 0',
        'change': '~/.config/eww/scripts/volume_script.py {}',
    }

vol_monitor = sp.Popen('pactl subscribe | grep --line-buffered "sink"', shell=True, text=True, stdout=sp.PIPE)

def output():
    vol = sp.getoutput('pamixer --get-volume')
    vol = vol if vol != '' else '0'
    icon = [v for k, v in icons.items()
            if k >= int(vol) or k == 100][0]
    icon_class = "icon" if int(vol) < 80 else "yellow-icon" if int(vol) < 90 else "orange-icon"
    print(
          '(eventbox :onhover `${EWW_CMD} update volume_reveal=true` :onhoverlost `${EWW_CMD} update volume_reveal=false`'
          f':onclick `{actions["max"]}` :onrightclick `{actions["mute"]}` :onscroll `{actions["change"]}` '
          f'(box :orientation "v" :space-evenly false :spacing 5 (label :class "{icon_class}" :text "{icon}") (revealer :reveal volume_reveal :transition "slidedown" "{vol}")))')

while True:
    output()
    sys.stdout.flush()
    vol_monitor.stdout.readline()
