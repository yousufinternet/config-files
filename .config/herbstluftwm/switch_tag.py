#!/usr/bin/env python
# Automatically executed when switching tags to move all sticky windows,
# keeping their minimized state
import subprocess as sp


def hc(*args):
    P = sp.Popen(
        f'herbstclient {" ".join(args)}', text=True, shell=True,
        stdout=sp.PIPE, stderr=sp.PIPE)
    err = not bool(P.stderr.read())
    out = P.stdout.read()
    return out, err


hc('lock')

clients = [wid.rstrip('.') for wid in
           hc('attr clients')[0].split() if wid.startswith('0x')]

sticky_clts = [
    wid for wid in clients
    if hc(f'get_attr clients.{wid}.my_sticky')[0].rstrip() == 'true'
]

for wid in sticky_clts:
    was_min = eval(hc(f'attr clients.{wid}.minimized')[0].title())
    hc(f'bring {wid}')
    if was_min:
        hc(f'set_attr clients.{wid}.minimized on')

hc('unlock')
