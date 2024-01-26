#!/usr/bin/env python

import re
import time
import subprocess as sp

duration = sp.check_output('rofi -dmenu -p "Enter desired period (m for minutes, h for hours):"', shell=True, text=True).strip()

if duration.isnumeric():
    time.sleep(int(duration))
elif duration.endswith('m'):
    duration = re.search(r'(\d+)', duration).group(1)
    time.sleep(int(float(duration)*60))
elif duration.endswith('h'):
    duration = re.search(r'(\d+)', duration).group(1)
    time.sleep(int(float(duration)*60*60))

sp.Popen('notify-send -a "Rofi Timer" "Timer finished" -i "/usr/share/icons/Papirus-Dark/symbolic/status/timer-symbolic.svg"', shell=True)

sp.Popen('cvlc --play-and-exit /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga', shell=True)
