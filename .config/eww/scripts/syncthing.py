#!/usr/bin/env python

import json
from io import StringIO
import subprocess as sp

def get_guiaddress():
    try:
        address = json.load(StringIO(sp.check_output(
            'syncthing cli show system',
            shell=True, text=True).strip()))['guiAddressUsed']
    except json.decoder.JSONDecodeError:
        address = 'localhost'
    return address

icon = '\uf021'
text = '0/0'

syncthing_json = sp.check_output('syncthing cli show connections', shell=True, text=True).strip()
icon_class = "grey-icon"
if syncthing_json:
    sync_conn = json.load(StringIO(syncthing_json))
    connected = len([v for v in sync_conn['connections'].values()
                    if v['connected']])
    text = f'{connected}/{len(sync_conn["connections"])}'
    icon_class = "green-icon" if connected > 0 else "grey-icon"
    icon = f'(label :class "{icon_class}" :text "{icon}")'
address = get_guiaddress()
print(f'(eventbox :valign "end" :vexpand false :onclick `xdg-open http://{address}` (box :valign "center" :vexpand false :orientation "h" :space-evenly false :spacing 5 {icon} "{text}"))')
