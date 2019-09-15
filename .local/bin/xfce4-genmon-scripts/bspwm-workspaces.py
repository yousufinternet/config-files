#!/usr/bin/env python

import subprocess
from functools import partial

cmd_output = partial(subprocess.check_output, text=True, shell=True)

all_workspaces = cmd_output('bspc query -D --names').strip().split('\n')
current = cmd_output('bspc query -D -d focused --names').strip()
try:
    urgent = cmd_output('bspc query -D -d .urgent --names').strip()
except subprocess.CalledProcessError:
    urgent = ''

# all_workspaces = [w if w != current else 
#                   + w +"</span>" for w in all_workspaces]

common_format =  "font_size='larger' font_weight='heavy'"
all_workspaces = '<txt> ' + ' | '.join(all_workspaces) + '  </txt>'
if urgent != '':
    all_workspaces = all_workspaces.replace(f' {urgent} ', f"<span underline='double' {common_format} bgcolor='Crimson' fgcolor='White'> {urgent} </span>" )
all_workspaces = all_workspaces.replace(
    f' {current} ',
    f"<span underline='single' bgcolor='Chocolate' {common_format} fgcolor='GhostWhite'> {current} </span>")

# multiple commands don't work, if I put bspc command only then it will be very ugly
all_workspaces += '<txtclick>bspc desktop next --focus</txtclick>'
print(all_workspaces)
