#!/usr/bin/env python

import subprocess as sp
from auto_move_sticky import execute

LISP_ARGS = ['(setq frame-title-format "EmacsAgenda")', '(org-agenda nil "a")',
             '(delete-other-windows)']
LISP_ARGS = '-e '+'-e '.join(f"'{a}'" for a in LISP_ARGS)
AGENDA_CMD = f"emacsclient -c -q -a '' {LISP_ARGS}"

print(AGENDA_CMD)
sp.Popen(AGENDA_CMD, shell=True, text=True)

for line in execute('herbstclient -c 10 --idle window_title_changed'):
    line = [i.strip() for i in line.split()]
    if line[0] == 'window_title_changed' and line[-1] == 'EmacsAgenda':
        sp.Popen(f'herbstclient apply_tmp_rule {line[1]} title=EmacsAgenda tag=AGENDA', shell=True, text=True)
        break
    
