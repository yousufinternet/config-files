#!/usr/bin/env python
import sys
import pysrt
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI('http://beelinkserver:5000')

src_lg = 'en' if len(sys.argv) < 3 else sys.argv[2]
dest_lg = 'ar' if len(sys.argv) < 4 else sys.argv[3]

sub_file = pysrt.open(sys.argv[1])
for sub in sub_file:
    sub.text = sub.text.replace('\n', ' ')
    sub.text = lt.translate(sub.text, src_lg, dest_lg)

sub_file.save(sys.argv[1])
