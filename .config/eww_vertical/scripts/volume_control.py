#!/usr/bin/env python
import subprocess as sp

icons = {0: '\uf026', 25: '\uf027', 100: '\uf028'}
actions = {
        'max': 'pactl set-sink-volume @DEFAULT_SINK@ 100%',
        'mute': 'pactl set-sink-volume @DEFAULT_SINK@ 0',
        'change': '~/.config/eww/scripts/volume_script.py {}',
    }

def output():
    vol = sp.getoutput('pamixer --get-volume')
    vol = vol if vol != '' else '0'
    prefix = ('%{A3:pactlmax:}%{A:pactlmute:}%{A4:pactlincrease:}'
                '%{A5:pactldecrease:}')

    icon = [v for k, v in icons.items()
            if k >= int(vol) or k == 100][0]
    print(
        '(eventbox :vexpand true :valign "center" :onhover `${EWW_CMD} update volume_reveal=true` :onhoverlost `${EWW_CMD} update volume_reveal=false` '
          f'(box :space-evenly false :spacing 5 :orientation "v" (eventbox :onclick `{actions["max"]}` :onrightclick `{actions["mute"]}` :onscroll `{actions["change"]}` '
          f'(box :orientation "v" :space-evenly false :spacing 5 (label :class "icon" :text "{icon}") "{vol}")) '
          f'(revealer :transition "slidedown" :reveal volume_reveal (scale :orientation "v" :draw-value false :min 0 :max 100 :value {int(vol)} :onchange `volume_ctl.sh {{}}` :round-digits 0))))')

output()
