#!/usr/bin/env python

import os
import pathlib
import subprocess as sp


lock_fp = os.path.expanduser('~/.config/eww/scripts/calendarlock')
if os.path.exists(lock_fp):
    sp.Popen('eww close calendar_pop', shell=True)
    os.remove(lock_fp)
else:
    pathlib.Path(lock_fp).touch()
    sp.Popen('eww open calendar_pop', shell=True)

