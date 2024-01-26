#!/usr/bin/env python

import os
import pyperclip
import subprocess as sp

PID = sp.check_output("xprop -id `xdotool getwindowfocus` | grep '_NET_WM_PID' | grep -oE '[[:digit:]]*$'", shell=True, text=True)
PID = PID.strip()
pagenumber = sp.check_output(f"qdbus org.pwmt.zathura.PID-{PID} /org/pwmt/zathura org.pwmt.zathura.pagenumber", shell=True, text=True)
filepath = sp.check_output(f"qdbus org.pwmt.zathura.PID-{PID} /org/pwmt/zathura org.pwmt.zathura.filename", shell=True, text=True)

filepath = filepath.strip()
pagenumber = int(pagenumber.strip()) + 1
fn = os.path.basename(filepath)
fn = '.'.join(fn.split('.')[:-1])[:10]+('...' if len(fn) > 10 else '.')+fn.split('.')[-1]
pyperclip.copy(f'[[file:{filepath}::{pagenumber}][{fn}:{pagenumber}]]')
sp.Popen(f'notify-send -a "Link copied!" "{fn}:{pagenumber}"', shell=True)
