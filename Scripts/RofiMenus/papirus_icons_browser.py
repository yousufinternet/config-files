#!/usr/bin/env python

import os
import sys
import subprocess as sp
from functools import partial
from collections import defaultdict

cmdout = partial(sp.check_output, shell=True, text=True)
cmdrun = partial(sp.Popen, shell=True, text=True, stdin=sp.PIPE, stdout=sp.PIPE)


ICON_THEME = '/usr/share/icons/Papirus-Dark'


def unique_icons():
    unique_icns = []
    unique_icns = defaultdict(list)
    for root, dirs, fns in os.walk(ICON_THEME):
        for fn in fns:
            if fn.endswith('svg') or fn.endswith('png'):
                icn_name = '.'.join(fn.split('.')[:-1])
                icn_path = os.path.join(root, fn)
                unique_icns[icn_name].append(icn_path)
    return unique_icns


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('\0prompt\x1fSearch icons:')
        print('\n'.join(f'{icn}\0icon\x1f{icn}' for icn in unique_icons().keys()))
    else:
        paths = '\n'.join(unique_icons()[sys.argv[1]])
        # for some reason pyperclip is causing rofi to hang
        cmdrun(f'echo "{paths}" | xclip -i -selection clipboard')
