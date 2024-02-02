#!/usr/bin/env python

import sys
import subprocess as sp

sp.Popen(f'pactl set-sink-volume @DEFAULT_SINK@ {"+" if sys.argv[1] == "up" else "-"}2%', shell=True)
