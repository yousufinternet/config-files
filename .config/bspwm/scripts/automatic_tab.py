#! /usr/bin/env python3
'''
Automatically add the new nodes to the focused tabbed instance
'''

from tabbed_company import add_win_to_tabbed, get_tabbed_children

from wmutils.utils import get_class, is_floating, is_fullscreen
from wmutils.processes import execute, cmd_output


def auto_tab_cond(event, last_wid):
    if any((is_floating(event[-1]), is_fullscreen(event[-1]))):
        return False
    if last_wid == '':
        return False
    win_class = get_class(last_wid)
    curwin_class = get_class(event[-1])
    if 'tabbed' in win_class and 'tabbed' not in curwin_class:
        # weird but children windows ids in a `tabbed` 
        # skip a `0` in window ids so it is 0x... instead of 0x0...
        # therefore the replace sentence
        was_tabbed_child = any(
            wid.lower() in children_ids for wid in
            (event[-1], event[-1].replace('0x0', '0x')))
        if not was_tabbed_child:
            return True
    else:
        return False


if __name__ == '__main__':
    children_ids = []
    for event in execute('bspc subscribe node_add node_focus'):
        event = event.split()
        if event[0] == 'node_add':
            last_wid = cmd_output('bspc query -N -d -n last.local.window')
            if auto_tab_cond(event, last_wid):
                add_win_to_tabbed(event[-1], last_wid)
        if event[0] == 'node_focus':
            node_id = event[-1]
            if 'tabbed' in get_class(node_id):
                children_ids = get_tabbed_children(node_id)
