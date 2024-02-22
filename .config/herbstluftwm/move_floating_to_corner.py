#!/usr/bin/env python

import sys
import subprocess as sp

from scratch import hc, repair_geometry, win_geometry, screen_dim, create_geometry_str


def get_floating_id():
    clients = sp.getoutput('herbstclient list_clients --floating').splitlines()
    clients = [c for c in clients if sp.getoutput(f'herbstclient attr clients.{c}.visible').strip() == 'true']
    if clients:
        return clients[0]
    return None


def main():
    wid = get_floating_id()
    print(wid)
    if not wid:
        return
    screen_dims = screen_dim()
    print(screen_dims)
    win_gmt = win_geometry(wid)
    print(win_gmt)
    max_x = screen_dims['x'] + screen_dims['width'] - win_gmt['width']-5
    max_y = screen_dims['y'] + screen_dims['height'] - win_gmt['height']-5
    corners = [(5, max_y), (max_x, max_y), (5, 5), (max_x, 5)]
    print(corners)
    print((win_gmt['x_pos'], win_gmt['y_pos']))
    # get the quarter of the screen the window is residing in
    win_x_center = win_gmt['x_pos'] + win_gmt['width']/2
    win_y_center = win_gmt['y_pos'] + win_gmt['height']/2
    screen_x_center = screen_dims['x'] + screen_dims['width']/2
    screen_y_center = screen_dims['y'] + screen_dims['height']/2
    print(win_gmt['x_pos'], win_x_center, win_gmt['y_pos'], win_y_center, screen_x_center, screen_y_center)
    if win_x_center < screen_x_center and win_y_center < screen_y_center:
        i = 0
    elif win_x_center < screen_x_center and win_y_center > screen_y_center:
        i = 1
    elif win_x_center > screen_x_center and win_y_center > screen_y_center:
        i = 3
    elif win_x_center > screen_x_center and win_y_center < screen_y_center:
        i = 2
    print(i)
    # if (win_gmt['x_pos'], win_gmt['y_pos']) in corners:
    #     i = corners.index((win_gmt['x_pos'], win_gmt['y_pos']))
    #     print(i, len(corners))
    #     i = i+move_dir if 0 <= i+move_dir < len(corners) else (0 if move_dir == 1 else -1)
    # else:
    #     i = 0
    new_x, new_y = corners[i]
    gmt_str = create_geometry_str(new_x, new_y, win_gmt['width'], win_gmt['height'])
    repair_geometry(wid, gmt_str)


if __name__ == '__main__':
    main()
