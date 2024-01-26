#!/usr/bin/env python

import sys
import time
import threading
import subprocess

def main(brightness):
    thread = threading.Thread(target=gradual_inrease, args=[brightness])
    thread.start()


def gradual_inrease(brightness):
    if not brightness:
        brightness = subprocess.check_output(['xbacklight', '-getf'])
        brightness = int(float(brightness.strip()))
    monitors = subprocess.check_output('xrandr', text=True)
    monitors = len([l for l in monitors.splitlines()[1:] if l[0] != ' ' and l.split()[1] == 'connected'])

    if brightness >= 50 :
        for i in range(brightness, 2,-1):
            time.sleep(0.02)
            subprocess.Popen(['xbacklight', str(i)])
        if monitors > 1:
            try:
                subprocess.Popen('sudo ddccontrol -r 0x10 -w 0 dev:/dev/i2c-4'.split())
            except:
                pass
    else:
        for i in range(brightness, 101,1):
            time.sleep(0.02)
            subprocess.Popen(['xbacklight', str(i)])
        if monitors > 1:
            try:
                subprocess.Popen('sudo ddccontrol -r 0x10 -w 75 dev:/dev/i2c-4'.split())
            except:
                pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        brightness = int(sys.argv[1])
    else:
        brightness = None
    main(brightness)
