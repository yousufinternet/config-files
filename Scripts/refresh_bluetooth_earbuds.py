#!/usr/bin/env python

import time
import subprocess as sp
from functools import partial

pods_mac = '88:D0:39:ED:EA:64'
run = partial(sp.Popen, shell=True, text=True)

run('rfkill block bluetooth')
run('bluetoothctl power off')
run('rfkill unblock bluetooth')

bluecmds = [
    'power on',
    'default-agent',
    f"cancel-pairing '{pods_mac}'",
    "scan on",
    f"pair '{pods_mac}'",
    f"trust '{pods_mac}'",
    f"connect '{pods_mac}",
    "scan off"
]

time.sleep(1)

P = sp.Popen('bluetoothctl', stdin=sp.PIPE)
P.communicate(input='\n'.join(bluecmds).encode())
