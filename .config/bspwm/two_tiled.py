#! /usr/bin/env python3

import os
import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

tiled_path = os.path.expanduser('~/.config/bspwm/tiled_desktops')


def rotate_if_horz(wins_no):
    if wins_no == 2:
        try:
            win = cmd_output('bspc query -N -n @north')
        except subprocess.CalledProcessError:
            win = ''
        try:
            win = cmd_output('bspc query -N -n @south')
        except subprocess.CalledProcessError:
            win = '' if win == '' else win
        if win != '':
            print('rotating!')
            cmd_run('bspc node @/ --rotate 90')

def get_wins_number():
    try:
        wins_no = len(cmd_output(
            'bspc query -N -n .local.window.!hidden.!floating.!fullscreen'
        ).strip().split('\n'))
        return wins_no
    except subprocess.CalledProcessError:
        return 0


def current_desktop_tiled():
    monitor_flag = False
    current_desktop = cmd_output('bspc query -D -d --names').strip()
    if os.path.exists(tiled_path):
        with open(tiled_path, 'r') as f_obj:
            for line in f_obj.readlines():
                # TODO: in future additional settings will be after
                # the desktop number therefore the split() thingy
                if current_desktop == line.strip().split()[0]:
                    # print(f'desktop {current_desktop}is tiled')
                    monitor_flag = True
                    break
                else:
                    monitor_flag = False
    return monitor_flag, current_desktop


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


# remove the tiled_path
if os.path.exists(tiled_path):
    os.remove(tiled_path)

for event in execute(['bspc', 'subscribe', 'all']):
    event = event.strip().split()
    # print(event) # use the logging module instead for better debugging
    monitor_flag, current_desktop = current_desktop_tiled()
    if not monitor_flag:
        continue
    wins_no = get_wins_number()
    # print('Windows number', end='\t')
    # print(wins_no)
    if event[0] in ['node_add']:
        wid = event[3]
        if not is_floating(wid):
            cmd_run(f'bspc node {wid} --flag private=on')
        try:
            last_window = cmd_output(
                'bspc query -N -n last.window.local').strip()
        except subprocess.CalledProcessError:
            last_window = ''
        print(last_window)
        if not last_window == '' and not wins_no <= 2:
            cmd_run(f'bspc node {last_window} --flag hidden=on')
            cmd_run(f'bspc node {last_window} --flag private=on')
        rotate_if_horz(get_wins_number())
    elif event[0] == 'node_remove':
        if not wins_no >= 2 and not is_floating(event[3]):
            try:
                a_hidden = cmd_output('bspc query -N -n any.hidden.local.window.!floating').strip()
            except subprocess.CalledProcessError:
                continue
            cmd_run(f'bspc node {a_hidden} --flag hidden=off')
            cmd_run(f'bspc node --focus {a_hidden}')
        rotate_if_horz(get_wins_number())
    # if the desktop is set to monocle and it was set as tiled already,
    # remove it from the tiled desktops file
    elif event[0] == 'node_flag':
        rotate_if_horz(get_wins_number())
    elif event[0] == 'desktop_layout':
        if event[2] == current_desktop and event[3] == 'monocle':
            cmd_run('set_tiled.py')




