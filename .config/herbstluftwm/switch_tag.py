#!/usr/bin/env python

import subprocess as sp


def hc(*args):
    P = sp.Popen(
        f'herbstclient {" ".join(args)}', text=True, shell=True,
        stdout=sp.PIPE, stderr=sp.PIPE)
    err = not bool(P.stderr.read())
    out = P.stdout.read()
    return out, err


hc('lock')

# cur_desk = hc('attr tags.focus.name')

clients = [wid.rstrip('.') for wid in
           hc('attr clients')[0].split() if wid.startswith('0x')]

sticky_clts = [
    wid for wid in clients
    if hc(f'get_attr clients.{wid}.my_sticky')[0].rstrip() == 'true']

cur_tag = hc('attr', 'tags.focus.name')[0].strip()
tag_clients = [
    wid for wid in clients if hc('attr', f'clients.{wid}.tag')[0].strip() == cur_tag
    and wid not in sticky_clts and hc('attr', f'clients.{wid}.visible')[0].strip() == 'true']
print(tag_clients)

for wid in sticky_clts:
    was_min = eval(hc(f'attr clients.{wid}.minimized')[0].title())
    hc(f'bring {wid}')
    # this was to bring focus back to tiled frames
    # hc('cycle_all +1')
    if was_min:
        hc(f'set_attr clients.{wid}.minimized on')
# focus = hc('attr', 'clients.focus.winid')
# focus_floating = hc('try attr', 'clients.focus.floating')[0].strip().title()
# if (focus_floating=='True' or focus in sticky_clts) and tag_clients:
if tag_clients and sticky_clts:
    # sp.Popen(f'notify-send {tag_clients}', text=True, shell=True)
    hc('jumpto', tag_clients[0])
    hc('raise', tag_clients[0])

hc('unlock')
