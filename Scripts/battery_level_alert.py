#!/usr/bin/env python

import subprocess as sp

thresh_critical = 10
thresh_warning = 25
early_warning = 50

battery = sp.getoutput('acpi --battery')
if battery != '':
    charging = 'Charging' in battery
    battery = battery.split(': ')[1].split(', ')[1]
    bat_vlu = int(battery.rstrip('%'))
    print(charging, bat_vlu)
    if not charging and bat_vlu <= thresh_critical:
        sp.Popen('notify-send -u "critical" -t 120000 -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-10-symbolic.svg" -a "Battery" "Battery level reached 10%, charge your laptop now"', shell=True)
    elif not charging and bat_vlu <= thresh_warning:
        sp.Popen('notify-send -u "normal" -t 60000 -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-20-symbolic.svg" -a "Battery" "Battery level reached 25%"', shell=True)
    elif not charging and bat_vlu <= early_warning:
        sp.Popen('notify-send -u "normal" -t 60000 -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-50-symbolic.svg" -a "Battery" "Battery level reached 50%"', shell=True)
    elif bat_vlu == 100:
        sp.Popen('notify-send -u "low" -i "/usr/share/icons/Papirus-Dark/symbolic/status/battery-level-100-charged-symbolic.svg" -a "Battery" "Battery is now fully charged"', shell=True)
