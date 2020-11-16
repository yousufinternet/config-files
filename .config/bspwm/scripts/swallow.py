#!/usr/bin/env python
'''
Swallow function for bspwm
when spawning a child process hide the parent process window
'''

import os
import sys
import json
import logging
import inspect
import traceback
import subprocess as sp

cmd_folder = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(os.path.join(cmd_folder, 'wmutils'))

from wmutils.processes import cmd_run, cmd_output, execute, is_child
from wmutils.utils import get_class, is_floating, is_fullscreen, desk_layout, get_pid


EXCLUDED_CLASSES = [
    'qutebrowser', 'xev', 'lemonbar', 'xfce4-panel', 'emacs', 'Emacs', 'Safeeyes', 'safeeyes'
]

logging_level = logging.ERROR if len(sys.argv) == 1 else sys.argv[1]
logging.basicConfig(filename=os.path.expanduser('~/.swallow.log'),
                    level=logging_level)


def node_crawler(prefix, node, path):
    if node is None:
        return
    if node['client'] is None:
        node_crawler(prefix, node['firstChild'], path+['1'])
        node_crawler(prefix, node['secondChild'], path+['2'])
    else:
        client = node['client']
        temp_paths[cmd_output(f'bspc query -N -n {node["id"]}')] = {
            'className': client['className'],
            'instanceName': client['instanceName'],
            'path': prefix + '/'.join(path)}


def capture_layout():
    global temp_paths
    temp_paths = {}
    state = json.load(cmd_run('bspc wm -d', stdout=sp.PIPE).stdout)
    for i, monitor in enumerate(state['monitors']):
        focused_desktop_id = monitor['focusedDesktopId']
        for j, desktop in enumerate(monitor['desktops']):
            if desktop['id'] == focused_desktop_id:
                node_crawler(f'@^{i+1}:^{j+1}:/', desktop['root'], [])


def advance_is_child(pid1, pid2):
    ps_out = [line.split(maxsplit=3) for line in
              cmd_output(f'ps --ppid {pid1}').split('\n')[1:]]
    print(ps_out)
    if any(line[-1] == 'tmux: client' for line in ps_out):
        tmux_shell_pid = cmd_output("tmux list-panes -F '#{pane_pid}'")
        print('tmux shell')
        print(tmux_shell_pid, pid2)
        return is_child(tmux_shell_pid, pid2)
    elif any(line[-1] == 'ranger' for line in ps_out):
        print(cmd_output(f'pstree -ls {pid2}').startswith('systemd---sh'))
        if cmd_output(f'pstree -ls {pid2}').startswith('systemd---sh'):
            return True
        return False
    else:
        return is_child(pid1, pid2)


def advance_is_child_depr(pid1, pid2):
    # TODO finish this
    # is this a terminal?
    ps_out = [line.split(maxsplit=3) for line in
              cmd_output(f'ps --ppid {pid1}').split('\n')[1:]]
    print(ps_out)
    ttys = {line[1]: (line[0], line[-1]) for line in ps_out if line[1] != '?'}
    print(ttys)
    if ttys:
        if any('tmux: client' in x[1] for x in ttys.values()):
            last_tmux_pid = cmd_output("tmux ")
            tmux_server_pid = cmd_output("pgrep 'tmux: server'")
            print(tmux_server_pid)
            ps_out = [line.split(maxsplit=3) for line in cmd_output(
                      f'ps --ppid {tmux_server_pid}').split('\n')[1:]]
            tmux_ttys = {line[1]: (line[0], line[-1]) for line in ps_out if line[1] != '?'}
            print(ps_out)
            print(tmux_ttys)
            for tty in ttys:
                tty_pid = tmux_ttys.get(tty, '')
                print(tty_pid)
                if tty_pid:
                    if is_child(tty_pid[0], pid2):
                        return True
        else:
            for tty_pid, _ in ttys.values():
                if is_child(tty_pid, pid2):
                    return True
    return False


def swallow_cond(new_wid, last_wid):
    '''
    True if window should be swallowed False if not
    Modify it to your liking
    '''
    print('swallow_cond')
    if desk_layout() == 'monocle':
        print(False)
        return False
    is_excluded = [c for c in EXCLUDED_CLASSES
                   if any(c in get_class(id)
                          for id in (new_wid, last_wid))]
    if is_excluded:
        return False
    if any((is_floating(new_wid), is_floating(last_wid),
            is_fullscreen(new_wid), is_fullscreen(last_wid),
            is_excluded)):
        return False
    return True


def swallow():
    '''
    monitore node_add and node_remove events and store swallowed
    windows in a dictionary
    '''
    swallowed = {}
    for event in execute('bspc subscribe node_add node_remove'):
        try:
            logging.debug(f'Processing Event: {event}')
            event = event.split()
            if not event:
                continue
            if event[0] == 'node_add':
                rotate_flag = False
                new_wid = event[-1]
                last_wid = cmd_output("bspc query -N -d -n 'last.window.!floating.!fullscreen'")
                if not swallow_cond(new_wid, last_wid):
                    continue
                new_pid = get_pid(new_wid)
                last_pid = get_pid(last_wid)
                if not all([new_pid, last_pid]):
                    continue
                if advance_is_child(last_pid, new_pid):
                    capture_layout()
                    last_path = temp_paths[last_wid]['path']
                    print(last_path)
                    new_path = last_path + '/1'
                    print(new_path)
                    cmd_run(f'bspc node {last_wid} --flag hidden=on')
                    cmd_run(f"bspc node {new_wid} --to-node {new_path}")
                    swallowed[new_wid] = last_wid
            if event[0] == 'node_remove':
                removed_wid = event[-1]
                if removed_wid in swallowed.keys():
                    swallowed_id = swallowed[removed_wid]
                    del swallowed[removed_wid]
                    cmd_run(f'bspc node {swallowed_id} --flag hidden=off')
                    cmd_run(f"bspc node {last_wid} --to-node {last_path}")
                    print(last_path.split(':')[-1])
                    if not len(last_path.split(':')[-1]) <= 5:
                        if last_path[-3] == '2':
                            cmd_run(f'bspc node {last_path[:-4]} --rotate 270')
                        else:
                            cmd_run(f'bspc node {last_path[:-4]} --rotate 90')
                    cmd_run(f'bspc node --focus {swallowed_id}')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            logging.debug('Error occured in mainloop:'
                          f'\n{e}\n{traceback.format_exc()}')


if __name__ == '__main__':
    try:
        swallow()
    except Exception as e:
        logging.debug('Error occured in mainloop:'
                      f'\n{e}\n{traceback.format_exc()}')
