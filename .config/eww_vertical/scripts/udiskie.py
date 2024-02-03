#!/usr/bin/env python

import subprocess as sp

def get_devices():
    info_lst = ['ui_device_label', 'is_mounted', 'is_external',
                'is_detachable', 'mount_path', 'device_size',
                'is_filesystem', 'is_partition', 'is_partition_table']
    info_cols = '\t'.join("{"+i+"}" for i in info_lst)
    info_cmd = (f'udiskie-info -o "{info_cols}" -a')
    udiskie_info = sp.getoutput(info_cmd)

    info_dict = {line.split(':')[0]: {
        c: ((i == "True") if i in ("True", "False") else i)
        for c, i in zip(info_lst, line.split(':')[1].split('\t'))}
                for line in udiskie_info.splitlines()}
    info_dict = {k: dct for k, dct in info_dict.items()
                 if dct['is_external'] and dct['is_filesystem']}
    return info_dict

devices = get_devices()
devices_str = ' '.join((f'(label :halign "center" :class "icon" :tooltip "{v["ui_device_label"]}" :text '+(r'"\\uf8e9"' if v['is_detachable'] else r'"\\uf0a0"')+')') for v in devices.values())
devices_str = devices_str if devices_str else '"No"'
final_str = f'(box :halign "center" :space-evenly false :spacing 5 :orientation "v" (label :halign "center" :class "icon" :text "\uf052") (revealer :halign "center" :reveal disks_reveal :transition "slidedown" (box :space-evenly false :spacing 5 :class "subwidget" {devices_str})))'
state = sp.getoutput('${EWW_CMD} get disks_reveal')
print(f'(eventbox :valign "center" :onclick {{disks_reveal ? `${{EWW_CMD}} update disks_reveal=false` : `${{EWW_CMD}} update disks_reveal=true`}} :onrightclick "rofi -show udiskie -modi udiskie:~/Scripts/RofiMenus/udiskie-menu.py &" {final_str})')
