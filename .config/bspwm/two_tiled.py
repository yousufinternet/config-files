#! /usr/bin/env python3

import os
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)


def is_floating(wid):
    try:
        cmd_output(f'bspc query -N -n {wid}.floating').strip()
        return True
    except subprocess.CalledProcessError:
        return False


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


tiled_path = os.path.expanduser('~/.config/bspwm/tiled_desktops')
os.remove(tiled_path)

for event in execute(['bspc', 'subscribe', 'all']):
    event = event.strip()
    print(event)
    monitor_flag = False
    if os.path.exists(tiled_path):
        current_desktop = cmd_output('bspc query -D -d --names').strip()
        with open(tiled_path, 'r') as f_obj:
            for line in f_obj.readlines():
                if current_desktop == line.strip().split()[0]:
                    print(f'desktop {current_desktop}is tiled')
                    monitor_flag = True
                    break
                else:
                    monitor_flag = False
    if not monitor_flag:
        continue
    try:
        wins_no = len(cmd_output('bspc query -N -n .local.window.!hidden.!floating.!fullscreen').strip().split('\n'))
    except subprocess.CalledProcessError:
        wins_no = 0
    print('Windows number')
    print(wins_no)
    if event.split()[0] in ['node_add']:
        wid = event.split()[3]
        if not is_floating(wid):
            cmd_run(f'bspc node {wid} --flag private=on')
        try:
            last_window = cmd_output('bspc query -N -n last.window.local').strip()
        except subprocess.CalledProcessError:
            last_window = ''
        print(last_window)
        if not last_window == '' and not wins_no <= 2:
            cmd_run(f'bspc node {last_window} --flag hidden=on')
            cmd_run(f'bspc node {last_window} --flag private=on')
    elif event.split()[0] == 'node_remove':
        if not wins_no >= 2 and not is_floating(event.split()[3]):
            # cmd_run('replace_with_hidden.py')
            try:
                a_hidden = cmd_output('bspc query -N -n any.hidden.local.window.!floating').strip()
            except subprocess.CalledProcessError:
                continue
            cmd_run(f'bspc node {a_hidden} --flag hidden=off')
            cmd_run(f'bspc node --focus {a_hidden}')
    elif event.split()[0] == 'desktop_layout':
        if event.split()[2] == current_desktop and event.split()[3] == 'monocle':
            cmd_run('set_tiled.py')




