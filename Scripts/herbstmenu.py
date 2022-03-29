#!/usr/bin/env python

import re
import sys
import subprocess as sp
from functools import partial

cmdout = partial(sp.check_output, text=True)
cmdrun = partial(sp.Popen, stdout=sp.DEVNULL, stderr=sp.DEVNULL)


def main(rofi_arg=None):
    print('\0no-custom\x1ftrue')
    print('\0prompt\x1fPick an action')
    if not rofi_arg:
        print('\0no-custom\x1ftrue')
        print('\0message\x1fPick or filter commands')
        commands = cmdout('herbstclient list_commands'.split())
        print(commands)
        sys.exit()
    else:
        args = ' '.join(rofi_arg)
        try:
            completions = cmdout(f'herbstclient complete {len(rofi_arg)} {args}'.split())
            print(completions)
        except sp.CalledProcessError:
            cmdrun(f'herbstclient {args}'.split())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
