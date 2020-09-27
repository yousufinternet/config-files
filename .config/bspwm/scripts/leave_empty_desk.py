#!/usr/bin/env python

import time
from wmutils.processes import cmd_run, cmd_output
from wmutils.utils import is_desk_empty, bspwm_events


events = bspwm_events('node_remove')
for event in events:
    if is_desk_empty(cmd_output("bspc query -D -d --names")):
        try:
            time.sleep(4)
            if is_desk_empty(cmd_output("bspc query -D -d --names")):
                cmd_run('bspc desktop --focus last.occupied')
        except Exception:
            pass
