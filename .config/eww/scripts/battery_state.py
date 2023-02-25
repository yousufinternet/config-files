#!/usr/bin/env python
import subprocess as sp


icons = {5: '\uf244', 25: '\uf243', 50: '\uf242',
         75: '\uf241', 100: '\uf240'}

battery = sp.getoutput('acpi --battery')
if battery != '':
    charging = 'Charging' in battery
    battery = battery.split(': ')[1].split(', ')[1]
    bat_vlu = int(battery.rstrip('%'))
    icon = [v for k, v in icons.items() if k >= bat_vlu][0]
    if bat_vlu <= 5:
        print(f'(box :space-evenly false :spacing 5 (label :class "red-icon" :text "{icon}") "{bat_vlu:0.0f}%")')
    elif bat_vlu == 100:
        print(f'(box :space-evenly false :spacing 5 (label :class "green-icon" :text "{icon}") "{bat_vlu:0.0f}%")')
    elif charging:
        print(f'(box :space-evenly false :spacing 5 (label :class "yellow-icon" :text "{icon}") "{bat_vlu:0.0f}%")')
    else:
        print(f'(box :space-evenly false :spacing 5 (label :class "icon" :text "{icon}") "{bat_vlu:0.0f}%")')
