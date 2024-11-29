#!/usr/bin/env python

import sys
import subprocess as sp

sp.Popen(f'volume_ctl.sh {"+" if sys.argv[1] == "up" else "-"}2', shell=True)
