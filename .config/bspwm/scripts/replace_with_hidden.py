#! /usr/bin/env python3

import os
import sys
import subprocess
from wmutils.processes import cmd_run, cmd_output

swap_flag = False
if len(sys.argv) == 2:
    swap_flag = sys.argv[1] == 'swap'

rofi_theme = os.getenv('ROFI_THEME')
hidden_windows = cmd_output(
    "bspc query -N -d -n '.hidden.local.window.!sticky'")

if len(hidden_windows.split('\n')) == 0:
    sys.exit()
elif len(hidden_windows.split('\n')) == 1:
    selected_window = hidden_windows
else:
    try:
        wins_titles = '\n'.join(
            [f'{i}|'+cmd_output('xtitle '+win_id)
             for i, win_id in enumerate(hidden_windows.split('\n'))])
        selected_window = cmd_output(
            f'echo "{wins_titles}" | rofi -dmenu -dpi 0 -theme {rofi_theme}')
        selected_window = hidden_windows.split('\n')[int(selected_window.split('|')[0])]
    except subprocess.CalledProcessError:
        sys.exit()

try:
    current_win = cmd_output('bspc query -N -n focused')
except subprocess.CalledProcessError:
    pass

cmd_run(f'bspc node {selected_window} --flag hidden=off')
cmd_run(f'bspc node {selected_window} --flag private=on')
if swap_flag:
    cmd_run(f'bspc node {current_win} --flag private=on')
    cmd_run(f'bspc node --swap {selected_window} --follow')
    cmd_run(f'bspc node {current_win} -g hidden=on')
    cmd_run(f'bspc node -f {selected_window}')
