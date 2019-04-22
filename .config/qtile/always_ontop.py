#!/usr/bin/env python
import os
import sys
from libqtile.command import Client


def ontop(title):
    c = Client()
    if title is None:
        title = c.group.window.info()['name']
        print(title)
        with open(PATH, 'w+') as f_obj:
            f_obj.write(title)
    wid = [(w['id'], w['group']) for w in c.windows() if title == w['name']]
    if len(wid) == 0:
        os.remove(PATH)
        return
    c.window[wid[0][0]].bring_to_front()
    c.window[wid[0][0]].togroup()

    # This code runs only when the current group is changed, so that
    # correct window is focused instead of mpv window
    prv_grp = wid[0][1]
    cur_grp = c.group.info()['name']
    focusHistory = c.groups()[c.group.info()['name']]['focusHistory']
    if focusHistory[-1] == title and cur_grp != prv_grp:
        last_wid = [w['id'] for w in c.windows() if w['name'] == focusHistory[-2]
                    and w['group'] == cur_grp][0]
        c.window[last_wid].focus()


if __name__ == '__main__':
    PATH = os.path.expanduser('~/.config/qtile/alwaysontop_win')
    if len(sys.argv) == 2:
        ontop(None)
    if os.path.exists(PATH):
        with open(PATH, 'r') as f_obj:
            title = f_obj.read()
        ontop(title)
