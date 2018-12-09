#!/usr/bin/env python

import datetime
import time
import os
import subprocess
import inspect

script_path = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
while True:
    current_hr = datetime.datetime.now().hour
    wall_no = round((current_hr/24) * 15) + 1
    wall_path = os.path.join(
        script_path, 'mojave_dynamic', 'mojave_dynamic_%s.jpeg' % wall_no)
    subprocess.Popen(['feh', '--bg-scale', wall_path])
    time.sleep(60)
