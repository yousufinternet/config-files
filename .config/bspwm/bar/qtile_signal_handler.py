#!/usr/bin/env python

import os
import sys
import time
import signal


def signal_handle(*args):
    sys.stdout.write('Event\n')
    sys.stdout.flush()


if __name__ == '__main__':
    with open('/tmp/qtile_signal_handler_pid', 'w+') as f_obj:
        f_obj.write(str(os.getpid()))
    signal.signal(signal.SIGUSR1, signal_handle)
    while True:
        time.sleep(0.1)
        with open('/tmp/qtile_signal_handler_pid', 'r') as f_obj:
            pid = f_obj.read().strip()
        if str(os.getpid()) != pid:
            sys.exit()
