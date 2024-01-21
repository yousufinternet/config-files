#!/usr/bin/env python

import os
import sys
import subprocess as sp

page = None
fp = os.path.expanduser(sys.argv[1])
if len(sys.argv) > 2:
    page = int(sys.argv[2])
try:
    zathura_instances = sp.check_output('qdbus | grep zathura', shell=True, text=True)
except sp.CalledProcessError:
    zathura_instances = ''

file_open = False
for zathura_instance in zathura_instances.strip().splitlines():
    inst_fp = sp.check_output(f'qdbus {zathura_instance.strip()} /org/pwmt/zathura org.pwmt.zathura.filename', shell=True, text=True)
    if inst_fp.strip() == fp:
        file_open = True
        break
if file_open and page is not None:
    sp.Popen(f'qdbus {zathura_instance} /org/pwmt/zathura org.pwmt.zathura.GotoPage {page-1}', shell=True)
elif not file_open and page is not None:
    sp.Popen(f"zathura '{fp}' -P {page}", shell=True)
else:
    sp.Popen(f'zathura --synctex-forward :: {fp}', shell=True)



