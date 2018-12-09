#!/usr/bin/env python
import threading
import time
import subprocess


def main():
    thread = threading.Thread(target=gradual_inrease)
    thread.start()


def gradual_inrease():
    brightness = subprocess.check_output(['light'])
    if float(brightness) >= 50 :
        for i in range(int(float(brightness[:-2])), 2,-1):
            time.sleep(0.02)
            subprocess.Popen(['light', '-S', str(i)])
    else:
        for i in range(round(float(brightness[:-2])), 101,1):
            time.sleep(0.02)
            subprocess.Popen(['light', '-S', str(i)])

if __name__ == '__main__':
    main()
