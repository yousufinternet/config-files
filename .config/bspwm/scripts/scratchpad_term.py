#!/usr/bin/env python

import os
import re
import argparse
from wmutils.processes import cmd_run, cmd_output
from wmutils.utils import screen_dim, win_geometry, get_class, is_hidden


def float_lt_zero(num):
    try:
        num = float(num)
    except ValueError:
        raise argparse.ArgumentError(f'Invalid {num} cannot convert to float')
    if num < 0:
        raise argparse.ArgumentError(f'{num} should not be less than 0')
    return num


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--termclass',
                        help='pass a class name for mlterm instance')
    parser.add_argument('-w', '--width', dest='width', default=0.5,
                        type=float_lt_zero, nargs='?',
                        help=('width in percent (pixels if more than 1) for'
                              ' the dropdown window (50% (0.5) by default)'))
    parser.add_argument('-ht', '--height', dest='height', default=0.5,
                        type=float_lt_zero, nargs='?',
                        help=('height in percent (pixels if less than 100) for'
                              ' the dropdown window (50% by default)'))
    parser.add_argument('-x', default=0, type=float_lt_zero)
    parser.add_argument('-y', default=0, type=float_lt_zero)
    parser.add_argument('--termflags', nargs=argparse.REMAINDER)
    return parser.parse_args()


def reapply_rule(win_class, geometry):
    'reapply the rule to make dropdown wins floating and sticky'
    flags = ('state=floating layer=above '
             f'private=on sticky=on rectangle={geometry}')
    new_rule = f'bspc rule -a {win_class} {flags}'
    fmt_rule = f'{win_class}:*:* => {flags}'
    if fmt_rule not in cmd_output('bspc rule -l').splitlines():
        cmd_run(new_rule)


def win_exists(win_class):
    'Return True (and window id) if window with a matching class is open'
    for wid in cmd_output('bspc query -N -n .window').split('\n'):
        if win_class in get_class(wid):
            return wid
    return False


def toggle_hide(wid):
    'toggle the hidden flag of the passed node'
    cmd_run(f'bspc node {wid} --flag hidden')
    if not is_hidden(wid):
        cmd_run(f'bspc node --focus {wid}')


def start_terminal(termclass, termargs):
    cmd_run(f'{os.getenv("TERMINAL")} -N {termclass} {" ".join(termargs)}')


def repair_geometry(wid, gmt):
    current = win_geometry(wid)
    screen_dims = screen_dim(cmd_output('bspc query -M -m --names'))
    re_obj = re.match(r'(\d+)x(\d+)([+-]\d+)([+-]\d+)', gmt)
    w,h,x,y = (float(re_obj.group(i)) for i in range(1,5))
    x = x+screen_dims['width'] if x < 0 else x
    y = y+screen_dims['height'] if y < 0 else y
    if w != current['width']:
        w_chg = w-current['width']
        cmd_run(f'bspc node {wid} --resize right {w_chg} 0')
    if h != current['height']:
        h_chg = current['height']-h
        cmd_run(f'bspc node {wid} --resize top 0 {h_chg}')
    if x != current['x_pos']:
        x_chg = x-current['x_pos']
        cmd_run(f'bspc node {wid} --move {x_chg} 0')
    if y != current['y_pos']:
        y_chg = y-current['y_pos']
        cmd_run(f'bspc node {wid} --move 0 {y_chg}')


def create_geometry_str(x, y, w, h):
    screen_dims = screen_dim(cmd_output('bspc query -M -m --names'))
    if x <= 1:
        x *= screen_dims['width']
    if y <= 1:
        y *= screen_dims['height']
    if w <= 1:
        w *= screen_dims['width']
    if h <= 1:
        h *= screen_dims['height']
    return f'{w:0.0f}x{h:0.0f}{x:+0.0f}{y:+0.0f}'


def main():
    args = parse_args()
    geometry = create_geometry_str(args.x, args.y, args.width, args.height)
    reapply_rule(args.termclass, geometry)
    wid = win_exists(args.termclass)
    if not wid:
        start_terminal(args.termclass, args.termflags)
    else:
        repair_geometry(wid, geometry)
        toggle_hide(wid)


if __name__ == '__main__':
    main()
