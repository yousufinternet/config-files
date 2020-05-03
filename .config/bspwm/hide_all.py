#! /usr/bin/env python3

import sys
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)


def hideall():
    focused = cmd_output('bspc query -N -n ".!hidden.window.focused" -d focused')
    for win in cmd_output('bspc query -N -n ".!hidden.window" -d focused').strip().split('\n'):
        cmd_run(f'bspc node {win} -g hidden=on')


def hidedir(direction):
    prev = ''
    while prev != cmd_output('bspc query -N -n ".!hidden.window" -d focused'):
        prev = cmd_output('bspc query -N -n ".!hidden.window" -d focused')
        cmd_run('bspc node ' + direction + ' -g hidden=on')


hideall()
