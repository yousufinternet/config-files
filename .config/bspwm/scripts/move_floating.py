#! /usr/bin/env python3

import os
import sys
import inspect

cmd_folder = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(os.path.join(cmd_folder, 'wmutils'))

from wmutils.utils import win_geometry, screen_dim
from wmutils.processes import cmd_run, cmd_output

if __name__ == '__main__':
    wid = cmd_output("bspc query -N -d -n 'any.floating.window.!hidden'").strip()
    if wid == '':
        sys.exit()

    win_gt = win_geometry(wid)

    current_monitor = cmd_output('bspc query -M --names -m focused').strip()

    scr_dim = screen_dim(current_monitor)

    at_rightedge = win_gt['x_pos'] + win_gt['width'] == scr_dim['width']
    at_leftedge = win_gt['x_pos'] == 0
    at_bottom = win_gt['y_pos'] + win_gt['height'] == scr_dim['height']

    if (at_bottom and at_rightedge) or (at_bottom and at_leftedge):
        if at_rightedge:
            cmd_run(
                f'bspc node {wid} --move -{scr_dim["width"]-win_gt["width"]} 0'
            )
        elif at_leftedge:
            cmd_run(
                f'bspc node {wid} --move {scr_dim["width"]-win_gt["width"]} 0')
    else:
        cmd_run(
            f'bspc node {wid} --move '
            f'{scr_dim["width"]-win_gt["width"]-win_gt["x_pos"]} '
            f'{scr_dim["height"]-win_gt["height"]-win_gt["y_pos"]}'
        )
