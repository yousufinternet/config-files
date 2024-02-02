#!/usr/bin/env python

import sys
import time
import datetime

clock_faces = {0: '\ue381', 1: '\ue382', 2: '\ue383', 3: '\ue384', 4: '\ue385',
                5: '\ue386', 6: '\ue387', 7: '\ue388', 8: '\ue389', 9: '\ue38a',
                10: '\ue38b', 11: '\ue38c'}
while True:
    hr = datetime.datetime.now().hour
    hr = hr - 12 if hr >= 12 else hr
    print(clock_faces.get(hr, '\ue381'))
    sys.stdout.flush()
    time.sleep(60*10)

