#!/usr/bin/env python

import re
import sys
import subprocess as sp
from functools import partial

cmdout = partial(sp.check_output, shell=True, text=True)
cmdrun = partial(sp.Popen, shell=True, text=True,
                 stdout=sp.DEVNULL, stderr=sp.DEVNULL)


# in case: SUDO_ASKPASS="helper program" sudo -A nmcli general reload
# this will use a helper program for asking for password

# Imagining the final result
# if connected to wifi only: {green wifi icon} {signal strength} {middle click show additonal info} | {yellow ethernet icon} 
# if connected to wifi and ethernet: {green wifi icon} {signal strength} {middle click show additional info} | {green ethernet icon} {connection name}
# if connected to ethernet and wifi turned off: {red wifi icon} | {green ethernet icon}
# if networking is off: {red wifi icon} | {red ethernet icon}
# connected but no internet: orange color (in case limited state actually works)
# clicking on networking module
# if wifi is connected: turn off wifi, disconnect, connect to a different wifi else turn off wifi, connect to wifi network
# if wifi is off: turn on wifi
# turn off networking, or turn on networking if on
# Create wifi hotspot if wifi is on (needs investigation)
# edit connections > spawn nm-connection-editor

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


def get_general_state():
    """
    STATE can be:
    none: the host is not connected to any network.
    portal: the host is behind a captive portal and cannot reach the full Internet.
    limited: the host is connected to a network, but it has no access to the Internet.
    full: the host is connected to a network and has full access to the Internet.
    unknown: the connectivity status cannot be found out.
    """
    nmcli_general = [l.split() for l in cmdout('nmcli general').splitlines()]
    return {col: val for col, val in zip(nmcli_general[0], nmcli_general[1])}
    

def lists_to_dict_table(text_table:list):
    """
    given a textual table, convert it to 
    """
    return {text_table[0][i]: [lst[i] for lst in text_table[1:]]
            for i in range(len(text_table[0]))}


def toggle_wifi(state):
    if state == 'on':
        cmdrun('nmcli radio wifi off')
    else:
        cmdrun('nmcli radio wifi on')


def toggle_networking(state):
    if state == 'on':
        cmdrun('nmcli networking off')
    else:
        cmdrun('nmcli networking on')


def get_active_connection():
    active_connection = cmdout('nmcli connection show --active').splitlines()
    return 


def get_devices_status():
    devices_table = [dev.split() for dev in cmdout('nmcli device').splitlines()]
    return lists_to_dict_table(devices_table)


def get_saved_connections():
    connections = cmdout('nmcli connection')
    return read_fwf(connections)


def get_wifi_networks(ifname):
    cmd = f'nmcli dev wifi list --rescan auto ifname {ifname}'
    wifi_aps = cmdout(cmd)
    return read_fwf(wifi_aps)


def perform_action(action, status, devices):
    ifname_rgx = re.compile(r'\[(.*?)\].*')
    if ifname_rgx.match(action):
        ifname = ifname_rgx.search(action).group(1)
        dev_idx = devices['DEVICE'].index(ifname)
        dev_info = {col: inf[dev_idx] for col, inf in devices.items()}
    if action == 'Edit connections':
        cmdrun('nm-connection-editor')
    elif action == 'Edit a connection':
        connections = get_saved_connections()
        for con in connections['NAME']:
            print(f'/edt/ {con}')
    elif action == 'Turn off networking':
        cmdrun('nmcli net off')
    elif action == 'Turn on networking':
        cmdrun('nmcli net on')
    elif action.endswith('Turn off WIFI'):
        cmdrun(f'nmcli radio wifi off ifname {ifname}')
    elif action.endswith('Turn on WIFI'):
        cmdrun(f'nmcli radio wifi on ifname {ifname}')
    elif action.endswith('Disconnect WIFI') or action.endswith('Disconnect'):
        cmdrun(f'nmcli device down {ifname}')
    elif action.endswith('Autoconnect WIFI'):
        cmdrun(f'nmcli device up {ifname}')
    elif any(action.endswith(act) for act in ['Activate a connection', 'Activate another connection']):
        connections = get_saved_connections()
        for i, con in enumerate(connections['NAME']):
            if connections['TYPE'][i] == dev_info['TYPE']:
                print(f'/con/ {con}')
    elif action.endswith('List access points') or action.endswith('Connect to a different AP'):
        aps = get_wifi_networks(ifname)
        for ap in aps['SSID']:
            print(f'/AP/ [{ifname}] {ap}')


def perform_sec_action(action):
    if action.startswith('/edt/'):
        connections = get_saved_connections()
        con_uuid = connections['UUID'][connections['NAME'].index(
            action.lstrip('/edt/ '))]
        cmdrun(f'nm-connection-editor -e {con_uuid}')
    elif action.startswith('/con/'):
        connections = get_saved_connections()
        con_uuid = connections['UUID'][connections['NAME'].index(
            action.lstrip('/con/ '))]
        cmdrun(f'nmcli con up {con_uuid}')
    elif action.startswith('/AP/'):
        ifname = action.split()[1].lstrip('[').rstrip(']')
        apname = ' '.join(action.split()[2:])
        cmdrun('konsole -e nmcli --ask device wifi connect'
               f' {apname} ifname {ifname}')


def main(rofi_arg=None):
    status = get_general_state()
    devices = get_devices_status()
    wifi_flag = True
    print('\0no-custom\x1ftrue')
    print('\0prompt\x1fPick an action')
    if not rofi_arg:
        if status['STATE'] != 'asleep':
            for i in range(len(devices['DEVICE'])):
                # ignore loopback
                if devices['DEVICE'][i] == 'lo':
                    continue
                if devices['TYPE'][i] == 'wifi' and devices['STATE'][i] == 'connected':
                    print(f'\0message\x1fWIFI connected to: <b>{devices["CONNECTION"][i]}</b>')
                    print(f'[{devices["DEVICE"][i]}] Disconnect WIFI\0icon\x1f'
                          'network-wireless-disconnected-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Activate another'
                          ' connection\0icon\x1fnetwork-wireless-no-route-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Connect to a different AP'
                          '\0icon\x1fnetwork-wireless-acquiring-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Turn off WIFI'
                          '\0icon\x1fnetwork-wireless-disconnected-symbolic')
                elif devices['TYPE'][i] == 'wifi' and devices['STATE'][i] == 'disconnected':
                    print(f'[{devices["DEVICE"][i]}] Autoconnect WIFI'
                          '\0icon\x1fnetwork-wireless-connected-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Activate a connection'
                          '\0icon\x1fnetwork-wireless-no-route-symbolic')
                    print(f'[{devices["DEVICE"][i]}] List access points'
                          '\0icon\x1fnetwork-wireless-acquiring-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Turn off WIFI'
                          '\0icon\x1fnetwork-wireless-disconnected-symbolic')
                elif devices['TYPE'][i] == 'wifi' and status['WIFI'] == 'disabled':
                    print(f'[{devices["DEVICE"][i]}] Turn on WIFI'
                          '\0icon\x1fnetwork-wireless')
                # if devices['TYPE'][i] == 'wifi' and status['WIFI'] == 'enabled':
                elif status['WIFI-HW'][i] == 'disabled' and wifi_flag:
                    print('\0message\x1fWIFI hardware switch is off')
                if (devices['TYPE'][i] == 'ethernet' and devices['STATE'][i] in [
                        'unavailable', 'disconnected']):
                    print(f'[{devices["DEVICE"][i]}] Activate a connection'
                          '\0icon\x1fnetwork-wired-symbolic')
                    print(f'[{devices["DEVICE"][i]}] Auto connect\0icon\x1f'
                          'network-wired-acquiring-symbolic')
                if devices['TYPE'][i] == 'ethernet' and devices['STATE'][i] == 'connected':
                    print(f'[{devices["DEVICE"][i]}] Disconnect\0icon\x1f'
                          'network-wired-offline-symbolic')
            print('Edit connections\0icon\x1fnetwork-workgroup')
            print('Edit a connection\0icon\x1fnetwork-connect')
            print('Turn off networking\0icon\x1fnetwork-disconnect')
        else:
            print('Turn on networking\0icon\x1fnetwork-workgroup')
        sys.exit()
    else:
        if rofi_arg.startswith('/'):
            perform_sec_action(rofi_arg)
        else:
            perform_action(rofi_arg, status, devices)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
