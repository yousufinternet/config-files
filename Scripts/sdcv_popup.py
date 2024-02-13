#!/usr/bin/env python

import pyperclip
import subprocess as sp

clipboard = pyperclip.paste()



title_change = sp.Popen('herbstclient --wait --count 1 window_title_changed', shell=True)
P = sp.Popen(f'konsole -p tabtitle="sdcv_translation" -p font="IBM Plex Mono Light,12.0" -p TerminalMargin=50 -p TerminalCenter=True -p LineSpacing=15 -p ScrollbarPosition=1 -p ScrollFullPage=True -e bash -c \'sdcv --color "{clipboard}"; read junk\'', text=True, shell=True)
title_change.wait()
sp.Popen('herbstclient apply_rules --all', shell=True)

