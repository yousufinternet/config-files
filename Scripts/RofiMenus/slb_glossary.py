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
sp.Popen(f'konsole --hold -e "echo \'{glossary[choice.strip()]}\'"', shell=True)
