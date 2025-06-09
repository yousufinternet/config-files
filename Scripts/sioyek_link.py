#!/usr/bin/env python

import sys
import pyperclip
import subprocess as sp

sp.Popen(f'notify-send "{sys.argv}"', shell=True)

fp = sys.argv[1]
fn = sys.argv[2]
page, x, y = sys.argv[3].split()

pyperclip.copy(f'[[file:{fp}::{page}][{fn}:{page}]]')
