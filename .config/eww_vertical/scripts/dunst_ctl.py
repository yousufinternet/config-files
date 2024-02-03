#!/usr/bin/env python

import sys
import subprocess as sp

paused = '\uf4b3'
notify = '\uf075'

notifications_monitor = sp.Popen('dbus-monitor "interface=\'org.freedesktop.Notifications\'" | grep --line-buffered "member=Notify"', stdout=sp.PIPE, text=True, shell=True)


def output_wrapper():
    is_paused = sp.check_output(['dunstctl', 'is-paused'], text=True).strip() == 'true'
    waiting = sp.check_output(['dunstctl', 'count'], text=True).strip().splitlines()[0].split(':')[1].strip()
    waiting = waiting if int(waiting) > 0 else ""

    icon_color = "grey-icon" if is_paused else "blue-icon"
    icon = f'(label :class "{icon_color}" :text "{paused if is_paused else notify}")'

    if waiting:
        icon = f'(box :orientation "v" :spacing 2 {icon} "{waiting}")'
    print(f'(eventbox :onclick `~/.config/eww/scripts/dunsttoggle.sh` :onrightclick `dunstctl history-pop` {icon})')

while True:
    output_wrapper()
    # print("(label :text 'test')")
    sys.stdout.flush()
    notifications_monitor.stdout.readline()

