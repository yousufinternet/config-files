#!/usr/bin/env python

import sys
import subprocess as sp

action = sys.argv[1]
players_list = sp.check_output(['playerctl', '-l'], text=True)

if action == "next":
    pass
elif action == "prev":
    pass
elif action == "current":
    pass
