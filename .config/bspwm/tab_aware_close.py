#! /usr/bin/env python3

import os
import sys
import subprocess
from tabbed_company import cmd_run, cmd_output, add_win_to_tabbed, get_class, get_tabbed_children


def confirm_close_tabbed(cur_wid):
    rofi_cmd = ('echo -e "yes\nno" | rofi -selected-row 1 -width 20% -dmenu'
                f' -dpi 0 -theme {os.getenv("ROFI_THEME")} -lines 2 -p "Do you'
                ' want to close all tabbed windows?"')
    try:
        win_class = get_class(cur_wid)
    except:
        win_class = []
    if 'tabbed' in get_class(cur_wid):
        if len(get_tabbed_children(cur_wid)) == 1:
            cmd_run(f'bspc node --{sys.argv[1]}')
        else:
            P = cmd_run(rofi_cmd, stdout=subprocess.PIPE)
            P.wait()
            answr = P.stdout.read().strip()
            if answr == 'yes':
                cmd_run(f'bspc node --{sys.argv[1]}')
    else:
        cmd_run(f'bspc node --{sys.argv[1]}')


if __name__ == '__main__':
    cur_wid = cmd_output('bspc query -N -n')
    if cur_wid and sys.argv[1] in ['kill', 'close']:
        confirm_close_tabbed(cur_wid)
