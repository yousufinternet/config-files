#!/usr/bin/env python
import sys
import json
import subprocess as sp

P = sp.Popen(
    "herbstclient --idle 'tag_changed|tag_flags'",
    text=True, shell=True, stdout=sp.PIPE, encoding='UTF-8')

tags_icns = {
    'WEB': '\uf0ac', 'DEV': '\uf5fc', 'TERM': '\uf120', 'DOCS': '\uf02d',
    'GIMP': '\uf1fc', 'READ': '\uf518', 'AGENDA': '\uf274',
    'DOWN': '\uf019', 'CHAT': '\uf086', 'GAME': '\uf11b'}

icns = True
numbers = False

def output():
    tags_status = sp.getoutput('herbstclient tag_status').strip()
    # format_dict = {':': 'color: white', '-': 'background-color: orange; color:black', '.': 'color:grey',
    #                 '!': 'color: red', '#': 'background-color: white; color: black'}
    format_dict = {':': 'icon', '-': 'alt-highlight-icon', '.': 'grey-icon',
                    '!': 'red-icon', '#': 'highlight-icon'}

    formatted_ws = []
    for i, w in enumerate(tags_status.split('\t')):
        if not w:
            continue
        wor = f' {w[1:]} '
        if icns and not numbers:
            wor = tags_icns.get(w[1:], '')
        elif numbers:
            wor = f' {i} ' 
        clr = format_dict.get(w[0], 'icon')
        formatted_ws.append({'ws_no': i, 'ws_icn': wor, 'ws_style': clr})

    json_obj = json.dumps(formatted_ws)
    print(json_obj)

if not sys.argv[1:]:
    while True:
        output()
        sys.stdout.flush()
        P.stdout.readline()
else:
    output()
    sys.stdout.flush()
