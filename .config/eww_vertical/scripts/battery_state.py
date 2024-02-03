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
    common_settings = ':halign "center" :vexpand true'
    if bat_vlu <= 5:
        print(f'(label {common_settings} :tooltip "{bat_vlu:0.0f}%" :class "red-icon" :text "{icon}")')
    if bat_vlu <= 20:
        print(f'(label {common_settings} :class "yellow-icon" :tooltip "{bat_vlu:0.0f}%" :text "{icon}")')
    elif bat_vlu >= 90:
        print(f'(label {common_settings} :tooltip "{bat_vlu:0.0f}%" :class "green-icon" :text "{icon}")')
    elif charging:
        print(f'(label {common_settings}:class "blue-icon" :tooltip "{bat_vlu:0.0f}%" :text "{icon}")')
    else:
        print(f'(label {common_settings} :tooltip "{bat_vlu:0.0f}%" :class "icon" :text "{icon}")')
