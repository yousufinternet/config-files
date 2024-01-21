#!/usr/bin/env python

import sys
import subprocess as sp
from functools import partial

cmdrun = partial(sp.Popen, shell=True, text=True,
                 stdout=sp.DEVNULL, stderr=sp.DEVNULL)
actions_dict = {
    'Logout': ('system-log-out-symbolic', 'herbstclient quit'),
    'Suspend': ('system-suspend-symbolic', 'systemctl suspend'),
    'Reboot': ('system-reboot-symbolic', 'sudo systemctl reboot --force'),
    'Power off': ('system-shutdown-symbolic', 'sudo systemctl poweroff --force'),
}

if len(sys.argv) < 2:
    print('\0no-custom\x1ftrue')
    print('\0message\x1fPlease select an action')
    for action, details in actions_dict.items():
        print(f'{action}\0icon\x1f{details[0]}')
else:
    # print(actions_dict[sys.argv[1]][1])
    cmdrun(actions_dict[sys.argv[1]][1])
