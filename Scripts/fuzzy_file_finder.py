#!/usr/bin/env python

import subprocess as sp

fp = sp.check_output('find ~ | rofi -dmenu -i -p "Files search"', shell=True, text=True)

sp.Popen(f"xdg-open '{fp}'")
