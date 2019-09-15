#! /usr/bin/env python3

import re
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

floating_id = cmd_output('bspc query -N -n any.floating.window.local').strip()
if floating_id == '':
    exit()

window_geometry = ' '.join(cmd_output(f'xwininfo -metric -shape -id {floating_id}').strip().split('\n')[2:8])

print(window_geometry)
regex_obj = re.search(r'Abs.*X.*?(-?\d+).*Abs.*Y.*?(-?\d+).*Width:\s+(\d+).*Height:\s+(\d+)', window_geometry)
# regex_obj = re.search(r'(\d+)x(\d+)\+?-?-?(\d+)\+?-?-?(\d+)', window_geometry)
window_geometry = {'x_pos': int(regex_obj.group(1)), 'y_pos': int(regex_obj.group(2)),
                   'width': int(regex_obj.group(3)), 'height': int(regex_obj.group(4))}


screen_dimensions = cmd_output('xrandr --listactivemonitors')
current_monitor = cmd_output('bspc query -M --names -m focused').strip()

regex_obj = re.search(current_monitor + r'\s+(\d{3,4})/\d+x(\d{3,4})',
                      screen_dimensions, flags=re.MULTILINE)
screen_dim = {'width': int(regex_obj.group(1)), 'height': int(regex_obj.group(2))}

at_rightedge = window_geometry['x_pos']+window_geometry['width'] == screen_dim['width']
at_leftedge = window_geometry['x_pos'] == 0
at_bottom = window_geometry['y_pos']+window_geometry['height'] == screen_dim['height']

if (at_bottom and at_rightedge) or (at_bottom and at_leftedge):
    if at_rightedge:
        cmd_run(f'bspc node {floating_id} --move -{screen_dim["width"]-window_geometry["width"]} 0')
    elif at_leftedge:
        cmd_run(f'bspc node {floating_id} --move {screen_dim["width"]-window_geometry["width"]} 0')
else:
    print(window_geometry)
    print(screen_dim)
    cmd_run(f'bspc node {floating_id} --move {screen_dim["width"]-window_geometry["width"]-window_geometry["x_pos"]} {screen_dim["height"]-window_geometry["height"]-window_geometry["y_pos"]}')

