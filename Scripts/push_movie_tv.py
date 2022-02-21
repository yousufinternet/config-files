#!/usr/bin/env python

import sys
import time
import subprocess as sp
from functools import partial

cmdout = partial(sp.check_output, shell=True, text=True)
cmdrun = partial(sp.Popen, shell=True, text=True)


devices = cmdout('adb devices')
if not '192.168.1.3' in devices:
    try:
        p = cmdrun('adb connect 192.168.1.3')
        p.wait()
    except sp.CalledProcessError:
        p = cmdrun('wol CC:A1:2B:B9:45:8A')
        p.wait()
        time.sleep(2)
        p = cmdrun('adb connect 192.168.1.3')
        p.wait()


storages = cmdout('adb -s 192.168.1.3 shell ls storage')
if not 'F65E1BDD5E1B9609' in storages:
    print('Drive not found, rebooting android device')
    cmdrun('adb -s 192.168.1.3 reboot')
    sys.exit()

if len(sys.argv) < 1:
    print('Please supply movie path')
P = cmdrun(f"adb -s 192.168.1.3 push '{sys.argv[1]}' /storage/F65E1BDD5E1B9609/Movies")
P.communicate()
