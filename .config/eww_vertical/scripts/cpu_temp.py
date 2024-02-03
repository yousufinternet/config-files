#!/usr/bin/env python
import sys
import subprocess as sp

icons_dict = {50: '\uf2cb', 60: '\uf2ca', 70: '\uf2c9',
              80: '\uf2c8', 90: '\uf2c7'}


sensors = sp.getoutput('sensors')
temps = [int(line.split()[2].split('.')[0]) for line in
         sensors.split('\n') if line.startswith('Core')]
avg_temp = sum(temps)/len(temps)
icon = [v for k, v in icons_dict.items() if k >= avg_temp or k == 90][0]
if avg_temp > 80:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "red-icon" :text "{icon}") "{avg_temp:.0f}" "CPU")')
elif avg_temp > 70:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "orange-icon" :text "{icon}") "{avg_temp:.0f}" "CPU")')
elif avg_temp > 60:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "yellow-icon" :text "{icon}") "{avg_temp:.0f}" "CPU")')
else:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "icon" :text "{icon}") "{avg_temp:.0f}" "CPU")')
