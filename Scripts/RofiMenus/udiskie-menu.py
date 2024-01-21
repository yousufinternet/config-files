#!/usr/bin/env python

import os
import sys
import json
import subprocess as sp
from functools import partial

cmdout = partial(sp.check_output, shell=True, text=True)
cmdrun = partial(sp.Popen, shell=True, text=True,
                 stdout=sp.DEVNULL, stderr=sp.DEVNULL)
TMP_INFO = os.path.expanduser('~/.config/rofi/.temp_udiskie_rofi_info')


def get_devices():
    info_lst = ['ui_device_label', 'is_mounted', 'is_external',
                'is_detachable', 'mount_path', 'device_size',
                'is_filesystem', 'is_partition', 'is_partition_table']
    info_cols = '\t'.join("{"+i+"}" for i in info_lst)
    info_cmd = (f'udiskie-info -o "{info_cols}" -a')
    udiskie_info = cmdout(info_cmd)

    info_dict = {line.split(':')[0]: {
        c: ((i == "True") if i in ("True", "False") else i)
        for c, i in zip(info_lst, line.split(':')[1].split('\t'))}
                for line in udiskie_info.splitlines()}
    info_dict = {k: dct for k, dct in info_dict.items()
                 if dct['is_external'] and dct['is_filesystem']}
    return info_dict


def path_if_mounted(inf_dict):
    if inf_dict["is_mounted"]:
        return inf_dict["mount_path"]
    return "Not mounted"


def perform_action(action):
    with open(TMP_INFO, 'r') as f:
        drive_info = json.load(f)
    if action == 'Unmount':
        cmdrun(f'udiskie-umount {drive_info["mount_path"]}')
    elif action == 'Mount':
        cmdrun(f'udiskie-mount {drive_info["dev_path"]}')
    elif action == 'Browse':
        cmdrun(f'konsole -e ranger "{drive_info["mount_path"]}"')
    elif action == 'Unpower':
        cmdrun(f'udiskie-umount -d {drive_info["dev_path"]}')
    elif action == 'Info':
        print('\n'.join(f'<b>{k}</b>: {v}' for k, v in drive_info.items()))
    elif action == 'Cancel':
        return


def main(rofi_arg=None):
    dev_info = get_devices()
    # Don't allow entering custom items, only listed items can be selected
    print('\0no-custom\x1ftrue\n')
    print('\0markup-rows\x1ftrue\n')

    # if no external devices were found
    if len(dev_info) < 1:
        print('\0message\x1fNo devices available\n')
        sys.exit()

    # rofi enteries
    enteries = [f'{k}: {v["ui_device_label"]}\t{path_if_mounted(v)}'
                for k, v in dev_info.items()]
    # add icons
    enteries_icons = [
        f'{ent}\0icon\x1f'+(
            'media-removable' if v['is_detachable']
            else 'drive-harddisk' if v['is_filesystem'] else 'device-usb'
        ) for ent, v in zip(enteries, dev_info.values())]

    if rofi_arg is not None:
        # when action is selected perform it
        if rofi_arg in ('Unmount', 'Mount', 'Unpower', 'Browse', 'Info', 'Cancel'):
            perform_action(sys.argv[1])
            os.remove(TMP_INFO)
            sys.exit()
        # when device is selected display list of options
        elif rofi_arg in enteries:
            # Grab selected device info
            selected_drive = enteries.index(sys.argv[1])
            drive_info = dev_info[list(dev_info.keys())[selected_drive]]
            drive_info['dev_path'] = list(dev_info.keys())[selected_drive]
            with open(TMP_INFO, 'w+') as f:
                json.dump(drive_info, f)
            if drive_info['is_filesystem']:
                print('Unpower\0icon\x1fnotification-device-eject')
                if drive_info['is_mounted']:
                    print('Unmount\0icon\x1fnotification-device-eject\nBrowse\0icon\x1ffolder')
                else:
                    print('Mount\0icon\x1fusb')
            print('Info\0icon\x1fhelp-info-symbolic\nCancel\0icon\x1fcancel')
        sys.exit()

    dmenu_str = '\n'.join(enteries_icons)
    print(dmenu_str)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
