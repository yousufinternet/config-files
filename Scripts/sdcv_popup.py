#!/usr/bin/env python

import pyperclip
import subprocess as sp

clipboard = pyperclip.paste()

sp.Popen(f'konsole -p tabtitle="sdcv_translation" -p font="monospace,20.0" -p TerminalMargin=150 -p TerminalCenter=True -p LineSpacing=15 -p ScrollbarPosition=1 -p ScrollFullPage=True -e bash -c \'sdcv --color "{clipboard}"; read junk\'', text=True, shell=True)

