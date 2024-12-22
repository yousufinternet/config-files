#!/usr/bin/env python
import sys
import socket, os

socket_path = os.path.join(os.getenv('XDG_RUNTIME_DIR'), "hypr", os.getenv('HYPRLAND_INSTANCE_SIGNATURE'), ".socket2.sock")
hyprland_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
hyprland_socket.settimeout(1)
hyprland_socket.connect(socket_path)
hyprland_socket.setblocking(True)

def output(layout='Eng'):
    print(
        '(eventbox :onclick `hyprctl switchxkblayout all next` '
        '(box :space-evenly false :spacing 0 :orientation "v" '
        f'(label :class "icon" :text "\uf11c") "{layout}"))')
    sys.stdout.flush()

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
    for event in data.splitlines(): 
       if event.startswith('activelayout'):
           layout = event.split('>>')[1].split(',')[1][:3]
           output(layout)
