#! /usr/bin/env python3

import subprocess
from functools import partial
from tabbed_company import cmd_output, execute, get_class, add_win_to_tabbed

cmd_run = partial(subprocess.Popen, text=True, shell=True)


def is_floating(wid):
    try:
        cmd_output(f'bspc query -N -n {wid}.floating').strip()
        return True
    except subprocess.CalledProcessError:
        return False


for event in execute('bspc subscribe all'):
    event = event.split()
    if event[0] == 'node_add':
        last_wid = cmd_output('bspc query -N -d -n last.window')
        try:
            win_class = get_class(last_wid)
        except:
            win_class = []
        if 'tabbed' in get_class(last_wid):
            add_win_to_tabbed(event[4], last_wid)
