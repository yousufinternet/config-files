#!/usr/bin/env python

import time
import subprocess as sp

P = sp.Popen('ssh root@openwrt adb tcpip 5555'.split())
P.wait()

time.sleep(2)
gateway = sp.check_output('ssh root@openwrt ip r', text=True, shell=True)
print(gateway)
gateway = gateway.splitlines()[0].split()[2]

P = sp.Popen(f'adb connect {gateway}'.split())
P.wait()
sp.Popen(f'scrcpy -s {gateway} -m 720 -f --max-fps 15'.split())
