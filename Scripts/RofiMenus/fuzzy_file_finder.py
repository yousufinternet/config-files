#!/usr/bin/env python

import subprocess as sp

fp = sp.check_output('find ~ -type f -not -path \'*/.*\' | rofi -dmenu -i -p "Files search"', shell=True, text=True)

sp.Popen(f"xdg-open '{fp.strip()}'", shell=True)
