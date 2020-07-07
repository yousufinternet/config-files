#!/usr/bin/env python
# Python version of the following code
# https://github.com/phenax/dotfiles/blob/master/.config/bspwm/scripts/resize.sh

import sys
from wmutils.utils import is_floating
from wmutils.processes import cmd_run, cmd_output

dir_ = sys.argv[1]
delta = 40 if len(sys.argv) < 3 else sys.argv[2]

x = f'+{delta}' if dir_ == 'right' else f'-{delta}' if dir_ == 'left' else '0'
y = f'+{delta}' if dir_ == 'down' else f'-{delta}' if dir_ == 'up' else '0'

pair_dict = {'right': 'left', 'left': 'right', 'top': 'bottom', 'bottom': 'top'}
DIR_ = 'right' if dir_ in ('left', 'right') else 'top'

FALLDIR = pair_dict[DIR_]

cmd_run(f'bspc node --resize {DIR_} {x} {y}')
if not is_floating(cmd_output('bspc query -N -n')):
    cmd_run(f'bspc node --resize {FALLDIR} {x} {y}')
