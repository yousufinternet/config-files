#!/usr/bin/env python

import os
import json
import subprocess as sp

with open(os.path.expanduser('~/Scripts/RofiMenus/glossary.json')) as f:
    glossary = json.load(f)

rofi_process = sp.Popen('rofi -matching regex -i -dmenu', shell=True, stdout=sp.PIPE, stdin=sp.PIPE)

rofi_process.stdin.write(str.encode('\n'.join(glossary.keys())))
rofi_process.wait()
choice = rofi_process.stdout.read()
choice = choice.decode('utf-8')
answer = glossary[choice.strip()].strip().replace("'", r"\'").replace('"', r'\"')
cmd = f'konsole --profile "Black-BigFont" --hold -e echo \'{answer}\';read -n 1 Enter'
sp.Popen(cmd, shell=True)
