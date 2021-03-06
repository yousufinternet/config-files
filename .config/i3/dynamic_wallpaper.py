#!/usr/bin/env python

import datetime
import time
import os
import subprocess
import inspect
import pipes

script_path = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
bfr_chg_hr = 'first time'
while True:
    current_hr = datetime.datetime.now().hour
    wall_no = round((current_hr/24) * 15) + 1
    wall_path = os.path.join(
        script_path, 'mojave_dynamic', 'mojave_dynamic_%s.jpeg' % wall_no)
    print(wall_path)
    shell_esc_path = pipes.quote(wall_path)
    # subprocess.Popen(['feh', '--bg-scale', wall_path])
    p = subprocess.Popen('wal -s -i %s' % shell_esc_path, shell=True)
    p.wait()
    wal_oomox_colors = pipes.quote(os.path.expanduser('~/.cache/wal/colors-oomox'))
    if current_hr != bfr_chg_hr:
        subprocess.Popen('oomox-materia-cli -o wal -d true %s' % wal_oomox_colors, shell=True)
    bfr_chg_hr = datetime.datetime.now().hour
    time.sleep(400)
