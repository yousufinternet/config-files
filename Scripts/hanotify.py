#!/usr/bin/env python

import sys
import subprocess as sp

args = sys.stdin.read()
sp.Popen(f'notify-send -a homeassistant -i "/usr/share/icons/Papirus-Dark/symbolic/devices/network-server-symbolic.svg" {args}', shell=True, text=True)
