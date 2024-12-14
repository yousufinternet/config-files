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
    active_ws_other_monitors = [m["activeWorkspace"]["name"] for m in monitors_json]

    workspaces_icns = {
        '1': '\uf0ac', '2': '\uf5fc', '3': '\uf120', '4': '\uf02d',
        '5': '\uf1fc', '6': '\uf518', '7': '\uf274',
        '8': '\uf019', '9': '\uf086', '10': '\uf11b'}

    ws_with_windows = [wp["name"] for wp in wp_json if wp["windows"] > 0]
    wp_btns = []
    wp_form = '(eventbox :onclick `hyprctl dispatch workspace {wp}` (label :class "{icon_class}" :text "{wp_icon}"))'
    for wp in workspaces_icns:
        if wp == active_wp:
            wp_btns.append(wp_form.format(wp=wp, icon_class='highlight-icon', wp_icon=workspaces_icns[wp]))
        elif wp in active_ws_other_monitors:
            wp_btns.append(wp_form.format(wp=wp, icon_class='orange-icon', wp_icon=workspaces_icns[wp]))
        elif wp in ws_with_windows:
            wp_btns.append(wp_form.format(wp=wp, icon_class='icon', wp_icon=workspaces_icns[wp]))
        else:
            wp_btns.append(wp_form.format(wp=wp, icon_class='grey-icon', wp_icon=workspaces_icns[wp]))

    print(f'(box :orientation "v" :space-evenly true :spacing 2 {" ".join(wp_btns)})')
    sys.stdout.flush()


socket_path = os.path.join(os.getenv('XDG_RUNTIME_DIR'), "hypr", os.getenv('HYPRLAND_INSTANCE_SIGNATURE'), ".socket2.sock")
hyprland_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
hyprland_socket.settimeout(1)
hyprland_socket.connect(socket_path)
hyprland_socket.setblocking(True)

output()
while True:
    while True:
        data = ''
        try:
            data_chunk = hyprland_socket.recv(4096)
            if data_chunk:
                data += data_chunk.decode('UTF-8')
            if data.endswith('\n'):
                break
        except BlockingIOError:
            pass
    if any(any(ev in event for ev in ('workspace', 'focusedmon', 'monitor', 'openwindow', 'closewindow')) for event in data.splitlines()):
        output()

