import os
import re
import sys
import json
import inspect

cmd_folder = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(cmd_folder)

from processes import cmd_output, execute


def desk_layout():
    '''
    return True if desktop is monocle
    '''
    return json.loads(cmd_output('bspc query -T -d'))['layout']


def get_pid(wid):
    '''
    get window process id using xprop output
    '''
    out = cmd_output(f'xprop -id {wid} _NET_WM_PID')
    if out:
        return out.split(' = ')[1]
    else:
        return ''


def screen_dim(mon_name):
    '''
    given a monitor name return the screen dimensions
    '''
    screen_dimensions = cmd_output('xrandr --listactivemonitors')
    regex_obj = re.search(mon_name + r'\s+(\d{3,4})/\d+x(\d{3,4})',
                          screen_dimensions,
                          flags=re.MULTILINE)
    screen_dims = {
        'width': int(regex_obj.group(1)),
        'height': int(regex_obj.group(2))
    }
    return screen_dims


def win_geometry(wid):
    '''
    given a window id return geometry using xwininfo package
    (x_pos, y_pos, width, height) dictionary
    '''
    window_geometry = ' '.join(
        cmd_output(f'xwininfo -metric -shape -id {wid}').strip().split(
            '\n')[2:8])
    regex_obj = re.search(
        r'Abs.*X.*?(-?\d+).*Abs.*Y.*?(-?\d+).*Width:\s+(\d+).*Height:\s+(\d+)',
        window_geometry)
    window_geometry = {
        'x_pos': int(regex_obj.group(1)),
        'y_pos': int(regex_obj.group(2)),
        'width': int(regex_obj.group(3)),
        'height': int(regex_obj.group(4))
    }
    return window_geometry


def get_class(wid):
    '''
    get passed window id class using xprop output
    '''
    try:
        out = cmd_output(f'xprop -id {wid} WM_CLASS')
        wm_class = [wid.strip('"') for wid in out.split(' = ')[1].split(', ')]
        return wm_class
    except Exception:
        return []


def bspwm_events(event):
    'monitor the passed event in bspc subscribe'
    for evnt in execute(f'bspc subscribe {event}'):
        yield evnt


def is_desk_empty(desk):
    'check wether passed desk refers to an empty desk or not'
    # return cmd_output(f"bspc query -D -d '{desk}.!occupied'") != ''
    return cmd_output(f"bspc query -N -d {desk} -n '.window.!sticky'") == ''


def is_hidden(wid):
    '''
    check whether passed window id refers to a hidden window
    '''
    return cmd_output(f'bspc query -N -n {wid}.hidden') != ''


def is_fullscreen(wid):
    '''
    check whether passed window id refers to a fullscreen window
    '''
    return cmd_output(f'bspc query -N -n {wid}.fullscreen') != ''


def is_floating(wid):
    '''
    check whether passed window id refers to a floating window
    '''
    return cmd_output(f'bspc query -N -n {wid}.floating') != ''
