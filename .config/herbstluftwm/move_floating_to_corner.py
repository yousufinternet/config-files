#!/usr/bin/env python

import sys
import subprocess as sp

from scratch import hc, repair_geometry, win_geometry, screen_dim, create_geometry_str


def get_floating_id():
    clients = hc('list_clients --floating')
    clients = [c for c in clients if hc(f'attr clients.{c}.visible')[0].strip() == 'true']
    if clients:
        return clients[0]
    return None


def main():
    move_dir = 1 if len(sys.argv) == 1 else -1
    wid = get_floating_id()
    print(wid)
    if not wid:
        return
    screen_dims = screen_dim()
    print(screen_dims)
    win_gmt = win_geometry(wid)
    print(win_gmt)
    max_x = screen_dims['width'] - win_gmt['width']
    max_y = screen_dims['height'] - win_gmt['height']
    corners = [(0, max_y), (max_x, max_y), (0, 40), (max_x, 40)]
    print(corners)
    print((win_gmt['x_pos'], win_gmt['y_pos']))
    if (win_gmt['x_pos'], win_gmt['y_pos']) in corners:
        i = corners.index((win_gmt['x_pos'], win_gmt['y_pos']))
        print(i, len(corners))
        i = i+move_dir if 0 <= i+move_dir < len(corners) else (0 if move_dir == 1 else -1)
    else:
        i = 0
    new_x, new_y = corners[i]
    gmt_str = create_geometry_str(new_x, new_y, win_gmt['width'], win_gmt['height'])
    repair_geometry(wid, gmt_str)


if __name__ == '__main__':
    main()
