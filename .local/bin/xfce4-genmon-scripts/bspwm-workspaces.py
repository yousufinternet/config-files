#!/usr/bin/env python

import subprocess
from functools import partial

cmd_output = partial(subprocess.check_output, text=True, shell=True)

all_workspaces = cmd_output('bspc query -D --names').strip().split('\n')
empty_workspaces = []
for desk in all_workspaces:
    try:
        wins = cmd_output(f"bspc query -N -d {desk}")
    except:
        wins = []
    if len(wins) == 0:
        empty_workspaces.append(desk)
current = cmd_output('bspc query -D -d focused --names').strip()
try:
    urgent = cmd_output('bspc query -D -d .urgent --names').strip().split('\n')
except subprocess.CalledProcessError:
    urgent = ''

# all_workspaces = [w if w != current else 
#                   + w +"</span>" for w in all_workspaces]

common_format =  "font_size='larger' font_weight='heavy'"

all_txt = []
for desk in all_workspaces:
    if desk == current:
        all_txt.append(f"<span underline='single' bgcolor='Chocolate' {common_format} fgcolor='GhostWhite'> {desk} </span>")
    elif desk in urgent:
        all_txt.append(f"<span underline='double' {common_format} bgcolor='Crimson' fgcolor='White'> {desk} </span>")
    elif desk in empty_workspaces:
        all_txt.append(f"<span bgcolor='Teal' fgcolor='GhostWhite'> {desk} </span>")
    else:
        all_txt.append(f' {desk} ')


# all_workspaces = '<txt> ' + ' | '.join(all_workspaces) + '  </txt>'
# if urgent != '':
#     all_workspaces = all_workspaces.replace(f' {urgent} ', f"<span underline='double' {common_format} bgcolor='Crimson' fgcolor='White'> {urgent} </span>" )
# all_workspaces = all_workspaces.replace(
#     f' {current} ',
#     f"<span underline='single' bgcolor='Chocolate' {common_format} fgcolor='GhostWhite'> {current} </span>")

# multiple commands don't work, if I put bspc command only then it will be very ugly
all_txt = '<txt>' + ''.join(all_txt) + '</txt>'
all_txt += '<txtclick>bspc desktop next --focus</txtclick>'
print(all_txt)
