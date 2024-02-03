#!/usr/bin/env python

import time
import subprocess as sp

def get_class_ids(class_name):
    try:
        eww_ids = sp.check_output(f'xdo id -N "{class_name}"', text=True, shell=True).splitlines()
        return eww_ids
    except sp.CalledProcessError:
        return []

time.sleep(1)
class_names = ('Eww', 'eww-top_bar', 'eww-top_bar_2', 'eww-v_bar_2', 'eww-vertical_bar')
xfce_ids = sp.check_output(
    'xdo id -a xfce4-panel', text=True, shell=True).strip().splitlines()
eww_ids = []
for cls_name in class_names:
    eww_ids += get_class_ids(cls_name)

for i in xfce_ids:
    for e in eww_ids:
        sp.Popen(
            f'xdo below -t {i} {e}', text=True, shell=True)
