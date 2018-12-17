#!/usr/bin/env python

from requests import get
import sys
import os
import codecs
import subprocess
import pyperclip


tmp_file = os.path.expanduser('~/.newsboat/newsboat.html')
url = sys.argv[1]
content = get(url).text
browser = "surf -t ~/.config/qutebrowser/Dark-stylesheets/gruvbox-all-sites.css -z 1.5" if not len(sys.argv) > 3 else sys.argv[2]

# subprocess.Popen(browser.split() + [url])

try:
    from breadability.readable import Article as reader
    print
    doc = reader(content)
    article = doc.readable
except ImportError:
    from readability import Document
    doc = Document(content)
    article = doc.summary().replace('<html>', '<html><head><title>%s</title></head>' % doc.title())
article = article.replace('<div id="readabilityBody">', '<style>img {max-width: 100%; max-height: 100%;}</style><div id="readabilityBody" style="max-width: 55%; min-width: 20%; margin: auto; text-align: justify; font-size: 30px; font-family: bookerly, Serif">')

with codecs.open(tmp_file, 'w', 'utf-8') as target:
    target.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    target.write(article)

subprocess.Popen(browser.split() + [tmp_file])
pyperclip.copy(url)
