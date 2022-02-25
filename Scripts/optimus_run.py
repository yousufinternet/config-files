#!/usr/bin/env python

import sys
import subprocess as sp

try:
    if sp.check_output('pacman -Qe nvidia-prime', shell=True, text=True).strip():
        sp.Popen('notify-send "nvidia card is utilized"', text=True, shell=True)
        sp.Popen(f'prime-run {" ".join(sys.argv[1:])}', shell=True, text=True)
        exit()
except sp.CalledProcessError:
    sp.Popen(f'{" ".join(sys.argv[1:])}', shell=True, text=True)
