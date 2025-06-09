#!/usr/bin/env python

import os
import sys
import json
import subprocess as sp
from functools import partial

cmdrun = partial(sp.Popen, shell=True, text=True,
                 stdout=sp.DEVNULL, stderr=sp.DEVNULL)

with open(os.path.expanduser('~/Scripts/RofiMenus/efdp_content.json'), 'r') as f:
    efdp_content = json.load(f)


if len(sys.argv) < 2:
    print('\0no-custom\x1ftrue')
    print('\0message\x1fPlease select a topic')
    for ref, title, page in efdp_content:
        print(f'{ref} {title}')
else:
    # print(actions_dict[sys.argv[1]][1])
    page = [page for ref, title, page in efdp_content if f'{ref} {title}' == sys.argv[1]][0]
    cmdrun(f'okular --page {int(page)+2} "/home/yusuf/Documents/Ratawi/Development Plans/Second Revision/EFDP_v2.pdf"')
