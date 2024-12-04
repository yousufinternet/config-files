#!/usr/bin/env python
import sys
import json
import socket, os
import subprocess as sp
from io import StringIO

def output(icons=True, numbers=False):
    wp_json = sp.check_output('hyprctl -j workspaces', text=True, shell=True)
    wp_json = json.load(StringIO(wp_json))
    active_wp = sp.check_output('hyprctl -j activeworkspace', text=True, shell=True)
    active_wp = json.load(StringIO(active_wp))["name"]
    monitors_json = sp.check_output('hyprctl -j monitors', text=True, shell=True)
    monitors_json = json.load(StringIO(monitors_json))
    active_monitor = [m["id"] for m in monitors_json if m["focused"]]

    workspaces_icns = {
        '1': '\uf0ac', '2': '\uf5fc', '3': '\uf120', '4': '\uf02d',
        '5': '\uf1fc', '6': '\uf518', '7': '\uf274',
        '8': '\uf019', '9': '\uf086', '0': '\uf11b'}

    wps_with_windows = [wp["name"] for wp in wp_json if wp["windows"] > 0]
    wp_btns = ' '.join(f'(eventbox :onclick `hyprctl dispatch workspace {wp}` (label :class {"grey-icon" if wp not in wps_with_windows else "icon" if wp != active_wp else "highlight-icon" if } :text {workspaces_icns[wp]}))' for wp in workspaces_icns)
    print('(box :orientation "v" :space-evenly true :spacing 2 {})')
    sys.stdout.flush()


socket_path = os.path.join(os.getenv('XDG_RUNTIME_DIR'), "hypr", os.getenv('HYPRLAND_INSTANCE_SIGNATURE'), ".socket2.sock")
hyprland_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
hyprland_socket.settimeout(1)
hyprland_socket.connect(socket_path)
hyprland_socket.setblocking(True)

def output(layout='Eng'):
    print(
        '(eventbox :onclick `hyprctl switchxkblayout all next` '
        '(box :space-evenly false :spacing 0 :orientation "v" '
        f'(label :class "icon" :text "\\uf11c") "{layout}"))')
    sys.stdout.flush()
