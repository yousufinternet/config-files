#!/usr/bin/env python

import os
import pathlib
import subprocess as sp


lock_fp = os.path.expanduser('~/.config/eww/scripts/calendarlock')

active_bar = [w for w in sp.check_output('eww active-windows', shell=True, text=True).strip().splitlines() if 'top_bar' in w][0].split(':')[0]
calendar_window = 'calendar_pop_2' if active_bar == 'top_bar_2' else 'calendar_pop'
if os.path.exists(lock_fp):
    sp.Popen(f'eww close {calendar_window}', shell=True)
    os.remove(lock_fp)
else:
    pathlib.Path(lock_fp).touch()
    sp.Popen(f'eww open {calendar_window}', shell=True)

