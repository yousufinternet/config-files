#!/usr/bin/env python

import sys
import time
import subprocess as sp
from functools import partial

cmdout = partial(sp.check_output, shell=True, text=True)
cmdrun = partial(sp.Popen, shell=True, text=True)

TV_ADDRESS = 'TCL-TV'
devices = cmdout('adb devices')
if not '192.168.1.3' in devices:
    try:
        p = cmdrun(f'adb connect {TV_ADDRESS}')
        p.wait()
    except sp.CalledProcessError:
        p = cmdrun('wol CC:A1:2B:B9:45:8A')
        p.wait()
        time.sleep(2)
        p = cmdrun(f'adb connect {TV_ADDRESS}')
        p.wait()


storages = cmdout(f'adb -s {TV_ADDRESS} shell ls storage')
if not 'F65E1BDD5E1B9609' in storages:
    print('Drive not found, rebooting android device')
    cmdrun(f'adb -s {TV_ADDRESS} reboot')
    sys.exit()

if len(sys.argv) < 1:
    print('Please supply movie path')
P = cmdrun(f"adb -s {TV_ADDRESS} push '{sys.argv[1]}' /storage/F65E1BDD5E1B9609/Movies")
P.communicate()
