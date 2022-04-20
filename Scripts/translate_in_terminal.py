#!/usr/bin/env python

import sys
import shlex
import subprocess as sp

sp.Popen('herbstclient lock'.split())
sp.Popen(['konsole', '--hold', '-p', 'tabtitle="sdcv_translation"', '-p', 'HighlightScrolledLines=false', '-p', 'DimWhenInactive=false', '-e', 'sdcv', '--color', shlex.quote(" ".join(sys.argv[1:]))])
sp.Popen('herbstclient unlock'.split())
