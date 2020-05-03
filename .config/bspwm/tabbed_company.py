#! /usr/bin/env python3
import os
import re
import sys
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def cmd_output(cmd):
    try:
        out = subprocess.check_output(cmd, text=True, shell=True).strip()
    except Exception:
        out = ''
    return out


def get_tabbed_children(tabbed_id):
    out = cmd_output(f'xwininfo -id {tabbed_id} -children')
    split_wrd = 'child:' if 'child:' in out else 'children:'
    children = [win.strip().split()[0] for win in
                out.split(split_wrd)[1].split('\n') if win]
    return children


def tab_current_win(cur_wid):
    for out_line in execute('~/.local/bin/tabbed -c'):
        if out_line != '':
            break
    tabbed_wid = out_line.strip()
    cmd_run(f'xdotool windowreparent {cur_wid} {tabbed_wid}')
    return tabbed_wid


def add_win_to_tabbed(wid, tabbed_wid):
    cmd_run(f'xdotool windowreparent {wid} {tabbed_wid}')


def get_class(wid):
    out = cmd_output(f'xprop -id {wid}')
    wids = re.search(r'^wm_class\(string\)\s=\s(.*?)$', out,
                     flags=re.IGNORECASE | re.MULTILINE).group(1)
    wids = [wid.strip('"') for wid in wids.split(', ')]
    return wids


def rm_win_from_tabbed(wid):
    root_wid = cmd_output('xwininfo -root').split('\n')[0].split()[3]
    cmd_run(f'xdotool windowreparent {wid} {root_wid}')


def tab_all():
    all_wids = cmd_output(
        "bspc query -N -d -n '.window.!floating.!hidden'").split('\n')
    all_wids = [wid for wid in all_wids
                if 'tabbed' not in get_class(wid)]
    if all_wids:
        tabbed_wid = tab_current_win(all_wids[0])
        if len(all_wids) > 1:
            for wid in all_wids[1:]:
                add_win_to_tabbed(wid, tabbed_wid)


if __name__ == '__main__':
    cur_wid = cmd_output(
        "bspc query -N -d -n 'focused.window.!hidden.!floating'")
    if cur_wid:
        if sys.argv[1] == 'create':
            if 'tabbed' not in get_class(cur_wid):
                tab_current_win(cur_wid)
        elif sys.argv[1] == 'join':
            if 'tabbed' in get_class(sys.argv[2]):
                add_win_to_tabbed(cur_wid, sys.argv[2])
        elif sys.argv[1] == 'remove':
            rm_win_from_tabbed(get_tabbed_children(cur_wid)[0])
        elif sys.argv[1] == 'children':
            print(get_tabbed_children(cur_wid))
        elif sys.argv[1] == 'all':
            tab_all()
