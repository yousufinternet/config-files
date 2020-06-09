#!/usr/bin/env python

import re
import subprocess
from functools import partial


EXCLUDED_CLASSES = ['qutebrowser', 'xev']

cmd_run = partial(subprocess.Popen, text=True, shell=True)


def get_class(wid):
    try:
        out = cmd_output(f'xprop -id {wid}')
        wids = re.search(r'^wm_class\(string\)\s=\s(.*?)$', out,
                        flags=re.IGNORECASE | re.MULTILINE).group(1)
        wids = [wid.strip('"') for wid in wids.split(', ')][1]
        return wids
    except Exception:
        return ''


def cmd_output(cmd):
    try:
        out = subprocess.check_output(cmd, text=True, shell=True).strip()
    except Exception:
        out = ''
    return out


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def is_fullscreen(wid):
    return cmd_output(f'bspc query -N -n {wid}.fullscreen').strip()


def is_floating(wid):
    return cmd_output(f'bspc query -N -n {wid}.floating').strip()


def get_pid(wid):
    out = cmd_output(f'xprop -id {wid} | grep WM_PID')
    if out:
        return out.split(' = ')[1]
    else:
        return ''


def is_child(pid, child_pid):
    tree = cmd_output(f'pstree -T -p {pid}')
    for line in tree.split('\n'):
        if child_pid in line:
            return True
    return False


def swallow():
    swallowed = {}
    for event in execute('bspc subscribe all'):
        event = event.split()
        if event[0] == 'node_add':
            new_wid = event[-1]
            last_wid = cmd_output('bspc query -N -d -n last.window')
            is_excluded = [c for c in EXCLUDED_CLASSES
                           if any(c in get_class(id)
                                  for id in (new_wid, last_wid))]
            if any((is_floating(new_wid), is_floating(last_wid),
                    is_fullscreen(new_wid), is_fullscreen(last_wid),
                    is_excluded)):
                continue
            new_pid = get_pid(new_wid)
            last_pid = get_pid(last_wid)
            if not all([new_pid, last_pid]):
                continue
            if is_child(last_pid, new_pid):
                cmd_run(f'bspc node {last_wid} --flag private=on')
                cmd_run(f'bspc node --swap {last_wid} --follow')
                cmd_run(f'bspc node {last_wid} --flag hidden=on')
                cmd_run(f'bspc node {new_wid} --flag private=on')
                swallowed[new_wid] = last_wid
        if event[0] == 'node_remove':
            removed_wid = event[-1]
            if removed_wid in swallowed.keys():
                swallowed_id = swallowed[removed_wid]
                cmd_run(f'bspc node {swallowed_id} --flag hidden=off')
                cmd_run(f'bspc node --focus {swallowed_id}')


if __name__ == '__main__':
    swallow()
