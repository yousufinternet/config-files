#!/usr/bin/env python

import time
import subprocess as sp

time.sleep(1)
xfce_ids = sp.check_output(
    'xdo id -a xfce4-panel', text=True, shell=True).strip().splitlines()
try:
    eww_ids = sp.check_output('xdo id -N "Eww"', text=True, shell=True).splitlines()
except sp.CalledProcessError:
    pass
try:
    eww_ids = sp.check_output('xdo id -N "eww-top_bar"', text=True, shell=True).splitlines()
except sp.CalledProcessError:
    pass
try:
    eww_ids = sp.check_output('xdo id -N "eww-top_bar_2"', text=True, shell=True).splitlines()
except sp.CalledProcessError:
    pass
for i in xfce_ids:
    for e in eww_ids:
        sp.Popen(
            f'xdo below -t {i} {e}', text=True, shell=True)
