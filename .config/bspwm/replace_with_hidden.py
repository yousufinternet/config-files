#! /usr/bin/env python3

import os
import sys
import subprocess
from functools import partial

swap_flag = False
if len(sys.argv) == 2:
    swap_flag = sys.argv[1] == 'swap'
cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

rofi_dpi = os.getenv('ROFI_DPI')
rofi_theme = os.getenv('ROFI_THEME')
hidden_windows = cmd_output('bspc query -N -d focused -n .hidden.local.window').rstrip()
if len(hidden_windows.split('\n')) == 0:
    exit()
elif len(hidden_windows.split('\n')) == 1:
    selected_window = hidden_windows
else:
    try:
        windows_with_titles = '\n'.join(
            [str(i)+'|'+cmd_output('xtitle '+win_id).rstrip()
             for i, win_id in enumerate(hidden_windows.split('\n'))])
        selected_window = cmd_output(
            f'echo -e "{windows_with_titles}" | rofi -dmenu -dpi {rofi_dpi} -theme {rofi_theme}').rstrip()
        selected_window = hidden_windows.split('\n')[int(selected_window.split('|')[0])]
    except subprocess.CalledProcessError:
        exit()

try:
    current_win = cmd_output('bspc query -N -n focused').rstrip()
except subprocess.CalledProcessError:
    pass

cmd_run(f'bspc node {selected_window} --flag hidden=off')
if swap_flag:
    cmd_run(f'bspc node --swap {selected_window}')
cmd_run(f'bspc node -f {selected_window}')
if swap_flag:
    cmd_run(f'bspc node {current_win} -g hidden=on')
cmd_run(f'bspc node -f {selected_window}')
