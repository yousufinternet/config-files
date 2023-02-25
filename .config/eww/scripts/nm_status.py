#!/usr/bin/env python

import sys
import json
import subprocess as sp

exclude = []
wifi_icons = ['\uf6aa', '\uf6ab', '\uf1eb']

def read_fwf(text_table):
    """
    only works when the first row is columns with a single word
    """
    cols_row = text_table.splitlines()[0]
    columns = cols_row.split()
    cols_idxs = []
    for i, (col, colnxt) in enumerate(zip(columns, columns[1:])):
        cols_idxs.append((0 if i == 0 else cols_row.index(f' {col}')+1,
                     cols_row.index(f' {colnxt}')+1))
    # cols_widths = [(cols_row.index(c), cols_row.index(cnxt)) for c, cnxt in zip(columns, columns[1:])]
    cols_idxs.append((cols_row.index(f' {columns[-1]}')+1, -1))
    final_dict = {
        col: [l[col_idx[0] : col_idx[1]].strip() for l in
              text_table.splitlines()[1:]]
        for col, col_idx in zip(columns, cols_idxs)
    }
    return final_dict


def get_devices_status():
    devices_table = sp.getoutput('nmcli device')
    return read_fwf(devices_table)

def get_wifi_networks(ifname):
    cmd = f'nmcli dev wifi list --rescan no ifname {ifname}'
    wifi_aps = sp.getoutput(cmd)
    return read_fwf(wifi_aps)


try:
    devs = get_devices_status()
except IndexError:
    print('{}')
    sys.exit()

output = {}
for dev_name, dev_type, dev_state, dev_con in zip(
        devs['DEVICE'], devs['TYPE'], devs['STATE'], devs['CONNECTION']):
    if dev_name == 'lo' or dev_name in exclude:
        continue
    if dev_type == 'wifi' and dev_state == 'connected':
        wifi_nets = get_wifi_networks(dev_name)
        wifi_signal = int(wifi_nets['SIGNAL'][wifi_nets['SSID'].index(dev_con)])

        # wifi_icon = r'󰤟' if wifi_signal < 25 else r'󰤢' if wifi_signal < 50 else '󰤥' if wifi_signal < 75 else '󰤨'
        output[dev_name] = {'icon': r'\uf1eb', 'connection': f'{wifi_signal}% {dev_con}', 'color': 'green'}
        # output += bars
    elif dev_type == 'wifi' and dev_state == 'disconnected':
        output[dev_name] = {'icon': r'\uf1eb', 'connection': dev_con, 'color': 'orange'}
    elif dev_type == 'wifi' and dev_state in ['disabled', 'unavailable']:
        output[dev_name] = {'icon': r'\uf1eb', 'connection': dev_con, 'color': 'red'}
    elif dev_type == 'wifi' and dev_state == 'unmanaged':
        output[dev_name] = {'icon': r'\uf1eb', 'connection': dev_con, 'color': 'grey'}
    elif dev_type == 'ethernet' and dev_state == 'connected':
        output[dev_name] = {'icon': r'\uf796', 'connection': dev_con, 'color': 'green'}
    elif dev_type == 'ethernet' and dev_state == 'connecting':
        output[dev_name] = {'icon': r'\uf796', 'connection': dev_con, 'color': 'yellow'}
    elif dev_type == 'ethernet' and dev_state in ['unavailable', 'disconnected']:
        output[dev_name] = {'icon': r'\uf796', 'connection': dev_con, 'color': 'orange'}
    elif dev_type == 'ethernet' and dev_state == 'unmanaged':
        output[dev_name] = {'icon': r'\uf796', 'connection': dev_con, 'color': 'red'}
    elif dev_type == 'tun' and dev_state == 'connected (externally)':
        output[dev_name] = {'icon': r'\uf6ff', 'connection': dev_con, 'color': 'green'}
    elif dev_type == 'tun' and dev_state == 'disconnected':
        output[dev_name] = {'icon': r'\uf6ff', 'connection': dev_con, 'color': 'orange'}


def command(self, event):
    if event == 'NM_MENU':
        subprocess.Popen(
            'rofi -show nmcli -modi nmcli:~/Scripts/RofiMenus/nmcli-menu.py',
            shell=True, text=True)
    elif event.startswith('WIFIQR'):
        ifname = event.split("_")[-1]
        subprocess.Popen(f'konsole --hold -e nmcli dev wifi show ifname {ifname}', shell=True, text=True)
    elif event.startswith('NMIFINFO'):
        ifname = event.split("_")[-1]
        dev_info = cmd_output(f'nmcli dev show {ifname}')
        subprocess.Popen(f'dunstify -a "NetworkManager" "{ifname.upper()} INFO" "{dev_info}"',
                            shell=True, text=True)


if len(sys.argv) > 1 and sys.argv[1] == 'devices':
    print(json.dumps(list(output.keys())))
    sys.exit()
print(json.dumps(output))
