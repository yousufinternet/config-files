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

# The try block so that we ensure herbtluftwm always gets unlocked
try:
    clients = [wid.rstrip('.') for wid in
            hc('attr clients')[0].split() if wid.startswith('0x')]

    focused_client = hc('attr clients.focus.winid')
    focused_client = None if not focused_client[1] else focused_client[0].strip()
    sticky_clts = [
        wid for wid in clients
        if hc(f'get_attr clients.{wid}.my_sticky')[0].rstrip() == 'true'
    ]

    tiling_or_fullscreen = False
    for wid in sticky_clts:
        was_min = hc(f'attr clients.{wid}.minimized')[0].strip() == 'true'
        fullscreen = hc(f'attr clients.{wid}.fullscreen')[0].strip() == 'true'
        tiling = hc(f'attr clients.{wid}.floating')[0].strip() == 'false'
        tiling_or_fullscreen = any((tiling_or_fullscreen, fullscreen, tiling))
        hc(f'bring {wid}')
        if was_min:
            hc(f'set_attr clients.{wid}.minimized on')
    # switch to the originally focused window unless the sticky window is tiling or fullscreen
    if focused_client is not None and not tiling_or_fullscreen:
        hc(f'jumpto {focused_client}')
except Exception:
    pass

hc('unlock')
