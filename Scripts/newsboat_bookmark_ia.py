#!/usr/bin/env python

import sys
import pyperclip
import subprocess as sp

url = sys.argv[1]
title = sys.argv[2]
description = sys.argv[3]
feed_title = sys.argv[4]

pyperclip.copy(description)

org_url = f'org-protocol://capture?template=ia&url={url}&title={feed_title} - {title}'
emacs_cmd = f'emacsclient -a "" -c "{org_url}"'
sp.Popen(emacs_cmd, shell=True, text=True)
