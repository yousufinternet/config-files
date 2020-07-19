#! /usr/bin/env python3

import os
import re
import sys
import subprocess
from functools import partial
import xml.etree.ElementTree as ET

cmd_run = partial(subprocess.Popen, text=True, shell=True)
cmd_output = partial(subprocess.check_output, text=True, shell=True)

notify_xml = '~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-notifyd.xml'
root = ET.parse(os.path.expanduser(notify_xml)).getroot()

for prop in root.findall('property'):
    prop_name = prop.get('name')
    if prop_name == 'do-not-disturb':
        dont_disturb = prop.get('value')

try:
    fullscreen_wins = cmd_output('bspc query -N -d -n .fullscreen')
except:
    fullscreen_wins = []

try:
    mpv_wins = cmd_output('pgrep -a mpv')
except:
    mpv_wins = []

cam_num = re.search('cam(\d).strm', sys.argv[-1]).group(1)

if len(fullscreen_wins) == 0 and dont_disturb == 'false':
    for win in mpv_wins.strip().split('\n'):
        if 'security-cam-preview' in win:
            continue
        else:
            geometry='960x540+2880+1620'
            if '--video-rotate=90' in sys.argv:
                geometry = '540x960+3300+1200'
            cmd_run(f'mpv --mute=yes --profile=low-latency --no-terminal --length=10 --geometry={geometry} {" ".join(sys.argv[1:])}')
            # cmd_run(f'mpv --no-terminal --geometry={geometry} --length=5 {" ".join(sys.argv[1:])}')
else:
    cmd_run(f'notify-send "Motion: Security Camera #{cam_num} Event"')
