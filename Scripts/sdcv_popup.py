#!/usr/bin/env python

import pyperclip
import subprocess as sp

clipboard = pyperclip.paste()



title_change = sp.Popen('herbstclient --wait --count 1 window_title_changed', shell=True)
P = sp.Popen(f'konsole -p tabtitle="sdcv_translation" -p font="IBM Plex Mono,12.0" -p HighlightScrolledLines=False -p ColorScheme="Gruvbox" -p TerminalMargin=50 -p TerminalCenter=True -p LineSpacing=4 -p ScrollbarPosition=1 -p ScrollFullPage=True -e bash -c \'sdcv --color "{clipboard}" | most; read junk\'', text=True, shell=True)
title_change.wait()
sp.Popen('herbstclient apply_tmp_rule --all title~\'^sdcv.*Konsole$\' floating=on floatplacement=none floating_geometry=700x450+10+10', shell=True)
# sp.Popen('herbstclient apply_rules --all', shell=True)

