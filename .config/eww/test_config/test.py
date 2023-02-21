#!/usr/bin/env python

import sys
import time
import random

while True:
    print(random.randint(1, 100))
    sys.stdout.flush()
    time.sleep(1)
