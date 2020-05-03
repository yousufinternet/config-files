#! /usr/bin/env python3

import os
import logging
import argparse
import subprocess
from functools import partial

parser = argparse.ArgumentParser()
parser.add_argument('--logging-level',
                    choices=['notset', 'debug', 'info', 'warning', 'critical', 'error'],
                    default='critical')
args = parser.parse_args()
logging_level = args.logging_level.upper()
logging.basicConfig(
    filename=os.path.expanduser('~/.config/bspwm/two_tiled.log'),
    filemode='w+', level=getattr(logging, logging_level),
    format='%(levelname)s | %(asctime)s\n%(message)s\n')

logging.info('Started')
cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

tiled_path = os.path.expanduser('~/.config/bspwm/tiled_desktops')
logging.debug(f'tiled_path={tiled_path}')


def rotate_if_horz(wins_no):
    if wins_no == 2:
        try:
            win = cmd_output('bspc query -N -n @north')
        except subprocess.CalledProcessError:
            win = ''
            logging.error(f'inside rotate_if_horz func, no window @north, win={win}')
        try:
            win = cmd_output('bspc query -N -n @south')
        except subprocess.CalledProcessError:
            win = '' if win == '' else win
            logging.error(f'inside rotate_if_horz func, no window @south, win={win}')
        if win != '':
            logging.debug(f'rotating window {win} was found @north/south')
            try:
                cmd_run('bspc node @/ --rotate 90')
            except subprocess.CalledProcessError:
                logging.exception('Failed to run "bspc node @/ --rotate 90"')


def get_wins_number():
    try:
        wins_no = len(cmd_output(
            'bspc query -N -n .local.window.!hidden.!floating.!fullscreen'
        ).strip().split('\n'))
        logging.debug(f'not hidden, not floating and not fullscreen windows '
                      f'number has been requested, {wins_no} was returned')
        return wins_no
    except subprocess.CalledProcessError:
        logging.error('not hidden, not floating and not fullscreen windows '
                      'number has been requested, 0 was returned')
        return 0


def current_desktop_tiled():
    monitor_flag = False
    try:
        current_desktop = cmd_output('bspc query -D -d --names').strip()
    except subprocess.CalledProcessError:
        logging.critical(
            'Failed to get the name of the current desktop using '
            '"bspc query -D -d --names"')
        return monitor_flag, 1
    logging.debug(f'current_desktop={current_desktop}')
    if os.path.exists(tiled_path):
        logging.debug('tiled_path exists')
        with open(tiled_path, 'r') as f_obj:
            for line in f_obj.readlines():
                # TODO: in future additional settings will be after
                # the desktop number therefore the split() thingy
                if current_desktop == line.strip().split()[0]:
                    monitor_flag = True
                    logging.info(f'current_desktop {current_desktop} was '
                                 'found to be tiled')
                    break
                else:
                    monitor_flag = False
    return monitor_flag, current_desktop


def is_floating(wid):
    logging.info(f'checking floating status for window {wid}')
    try:
        cmd_output(f'bspc query -N -n {wid}.floating').strip()
        logging.info('it was floating')
        return True
    except subprocess.CalledProcessError:
        logging.exception(f'command "bspc query -N -n {wid}.floating" failed')
        return False


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


# remove the tiled_path
if os.path.exists(tiled_path):
    os.remove(tiled_path)

a_hidden = ''
last_window = ''
for event in execute(['bspc', 'subscribe', 'all']):
    event = event.strip().split()
    logging.debug(f'EVENT: {" ".join(event)}')
    monitor_flag, current_desktop = current_desktop_tiled()
    if not monitor_flag:
        logging.debug('current desktop was found to be not tilling, skipping event check')
        continue
    wins_no = get_wins_number()
    hidden_off, hidden_on = False, False
    if len(event) >= 6:
        logging.debug('A hiding or showing event is suspected')
        # TODO : a history file for windows order, although complicated, might solve some issues here
        evnt = ' '.join((event[0], event[4], event[5]))
        logging.debug(f'event without window ids: {evnt}')
        hidden_off = evnt == 'node_flag hidden off' and not event[3] == a_hidden
        hidden_on = evnt == 'node_flag hidden on' and not event[3] == last_window
        logging.debug('a window was showed, it was not the window (({a_hidden})) shown automatically by this script. hidden_off = {hidden_off}')
        logging.debug('a window was hidden, it is not the window (({last_window})) automatically hidden by this script hidden_on={hidden_on}')
    if event[0] in ['node_add'] or hidden_off:
        wid = event[3]
        logging.debug(f'a new window {wid} has ben added to the tiled desktop')
        if not is_floating(wid):
            cmd_run(f'bspc node {wid} --flag private=on')
            logging.debug(f'window was found to be not floating, and was successfully marked as private')
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
    elif event[0] == 'node_remove' or hidden_on:
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


logging.info('Finished')


