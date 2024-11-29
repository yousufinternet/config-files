#!/usr/bin/env python
import os
import sys
import subprocess as sp

monitor_process = sp.Popen("echo ~/.config/THEME_VARIANT | entr -nsrp 'echo theme changed'", shell=True, text=True, stdout=sp.PIPE)

light_icon = '\uf185'
dark_icon = '\uf186'
mode_path = os.path.expanduser('~/.config/THEME_VARIANT')

def output():
    if os.path.exists(mode_path):
        with open(mode_path) as f:
            current_mode = f.read().strip()
    else:
        current_mode = 'dark'
    isdark = current_mode == 'dark'
    print(f'(eventbox :onclick `~/Scripts/switch_dark_light.py` (box :spacing {{minor_spacing}} :space-evenly false :orientation "v" (label :class "{"highlight-icon" if isdark else "icon"}" :text "{dark_icon}") (label :class "{"icon" if isdark else "highlight-icon"}" :text "{light_icon}")))')
    sys.stdout.flush()

while True:
    output()
    monitor_process.stdout.readline()
