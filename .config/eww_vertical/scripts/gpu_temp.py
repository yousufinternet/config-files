#!/usr/bin/env python
import sys
import subprocess as sp

icons_dict = {50: '\uf2cb', 60: '\uf2ca', 70: '\uf2c9',
              80: '\uf2c8', 90: '\uf2c7'}


temp = sp.getoutput('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader')
temp = float(temp)
icon = [v for k, v in icons_dict.items() if k >= temp or k == 90][0]
if temp > 75:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "red-icon" :text "{icon}") "{temp:.0f} "GPU")')
if temp > 65:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "yellow-icon" :text "{icon}") "{temp:.0f} "GPU")')
else:
    print(f'(box :vexpand true :orientation "v" :space-evenly false :spacing 2 (label :class "icon" :text "{icon}") "{temp:.0f}" "GPU")')
