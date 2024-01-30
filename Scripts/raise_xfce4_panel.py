#!/usr/bin/env python

import time
import subprocess as sp

time.sleep(1)
xfce_ids = sp.check_output(
    'xdo id -a xfce4-panel', text=True, shell=True).strip().splitlines()
eww_ids = sp.check_output('xdo -i -N Eww', text=True, shell=True).splitlines()
for i in xfce_ids:
    for e in eww_ids:
        sp.Popen(
            f'xdo below -t {i} {e}', text=True, shell=True)
