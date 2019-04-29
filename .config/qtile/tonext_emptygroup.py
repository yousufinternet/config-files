#!/usr/bin/env python
from libqtile.command import Client


def toemptygroup():
    QTILE_CLIENT = Client()
    empty_groups = [grp for grp in QTILE_CLIENT.groups().keys()
                    if len(QTILE_CLIENT.groups()[grp]['windows']) == 0]
    if len(empty_groups) == 0:
        return
    QTILE_CLIENT.window.togroup(empty_groups[0])
    QTILE_CLIENT.screen.toggle_group(empty_groups[0])


if __name__ == '__main__':
    toemptygroup()
