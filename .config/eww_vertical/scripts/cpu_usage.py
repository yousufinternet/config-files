#!/usr/bin/env python

import subprocess as sp

icon = '\uf0e4'

cpu_usage = sum(float(i) for i in sp.getoutput(
    'mpstat -P ALL').split('\n')[3].split()[3:6])
if cpu_usage >= 85:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "red-icon" :text "{icon}") "{cpu_usage:.0f}%")')
elif cpu_usage >= 75:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "orange-icon" :text "{icon}") "{cpu_usage:.0f}%")')
elif cpu_usage >= 65:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "yellow-icon" :text "{icon}") "{cpu_usage:.0f}%")')
else:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "icon" :text "{icon}") "{cpu_usage:.0f}%")')

