#!/usr/bin/env python

import subprocess as sp

thresh_critical = 10
thresh_warning = 25

battery = sp.getoutput('acpi --battery')
if battery != '':
    charging = 'Charging' in battery
    battery = battery.split(': ')[1].split(', ')[1]
    bat_vlu = int(battery.rstrip('%'))
    if not charging and bat_vlu < thresh_critical:
        sp.Popen('notify-send -u "critical" -t 7200 -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-10-symbolic.svg" -a "Battery" "Battery level reached 10%, charge your laptop now"', shell=True)
    elif not charging and bat_vlu < thresh_warning:
        sp.Popen('notify-send -u "normal" -t 3600 -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-20-symbolic.svg" -a "Battery" "Battery level reached 25%"', shell=True)
