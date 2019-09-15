#! /usr/bin/env python3

import sys
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)


def hideall(direction):
    prev = ''
    while prev != cmd_output('bspc query -N -n ".!hidden.window" -d focused'):
        prev = cmd_output('bspc query -N -n ".!hidden.window" -d focused')
        cmd_run('bspc node ' + direction + ' -g hidden=on')


hideall(sys.argv[1])
