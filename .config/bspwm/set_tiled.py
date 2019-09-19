#! /usr/bin/env python3

import os
import json
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

tiled_desktops = []

tiled_path = os.path.expanduser('~/.config/bspwm/tiled_desktops')

def write_desktops():
    global tiled_desktops
    tiled_desktops = list(set(tiled_desktops))
    print(tiled_desktops)
    with open(tiled_path, 'w') as f_obj:
        f_obj.write('\n'.join(tiled_desktops))

current_desktop = cmd_output('bspc query -D -d --names').strip()

layout = json.loads(cmd_output('bspc query -T -d').strip())['layout']

if os.path.exists(tiled_path):
    with open(tiled_path, 'r') as f_obj:
        tiled_desktops = f_obj.read().strip().split('\n')
        tiled_desktops = list(set(tiled_desktops))
        print(tiled_desktops)

if current_desktop not in tiled_desktops:
    tiled_desktops.append(current_desktop)
    write_desktops()
else:
    tiled_desktops = [t for t in tiled_desktops if t != current_desktop]
    write_desktops()
    exit()

if layout == 'monocle':
    cmd_run('bspc desktop --layout next')






