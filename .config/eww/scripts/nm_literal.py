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


def output_wrapper():
    try:
        devs = get_devices_status()
    except IndexError:
        print('(label :class "dimmed" :text "loading...")')
        return
    if list(devs.keys())[0] == 'Error:':
        print('(label :class "dimmed" :text "loading...")')
        return
    output = '(eventbox :onclick "rofi -show nmmenu -modi nmmenu:~/Scripts/RofiMenus/nmcli-menu.py &" (box :space-evenly false :spacing 5 {}))'
    common_device = '(label :tooltip {dev_info} :class "{color}-icon" :text "{icon}")'
    eww_devs = []
    for dev_name, dev_type, dev_state, dev_con in zip(
            devs['DEVICE'], devs['TYPE'], devs['STATE'], devs['CONNECTION']):
        if dev_name == 'lo' or dev_name in exclude:
            continue
        if dev_type == 'wifi' and dev_state == 'connected':
            wifi_nets = get_wifi_networks(dev_name)
            wifi_signal = int(wifi_nets['SIGNAL'][wifi_nets['SSID'].index(dev_con)])

            # wifi_icon = r'󰤟' if wifi_signal < 25 else r'󰤢' if wifi_signal < 50 else '󰤥' if wifi_signal < 75 else '󰤨'
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='green', icon='\uf1eb', dev_info=f'"{dev_name}: {wifi_signal}% {dev_con}"'))
            # output += bars
        elif dev_type == 'wifi' and dev_state == 'disconnected':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='orange', icon='\uf1eb', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'wifi' and dev_state in ['disabled', 'unavailable']:
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='red', icon='\uf1eb', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'wifi' and dev_state == 'unmanaged':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='grey', icon='\uf1eb', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'ethernet' and dev_state == 'connected':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='green', icon='\uf796', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'ethernet' and dev_state == 'connecting':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='yellow', icon='\uf796', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'ethernet' and dev_state in ['unavailable', 'disconnected']:
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='orange', icon='\uf796', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'ethernet' and dev_state == 'unmanaged':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='red', icon='\uf796', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'tun' and dev_state in ['connected (externally)', 'connected']:
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='green', icon='\uf6ff', dev_info=f'"{dev_name}: {dev_con}"'))
        elif dev_type == 'tun' and dev_state == 'disconnected':
            eww_devs.append(common_device.format(int_idx=devs['DEVICE'].index(dev_name), color='orange', icon='\uf6ff', dev_info=f'"{dev_name}: {dev_con}"'))

    print(output.format(' '.join(eww_devs)))
    sys.stdout.flush()

nm_monitor = sp.Popen('nmcli monitor', stdout=sp.PIPE, text=True, shell=True)

while True:
    nm_monitor.stdout.readline()
    output_wrapper()
