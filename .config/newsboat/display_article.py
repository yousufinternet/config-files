#!/usr/bin/env python

import os
import sys
import codecs
import random
import subprocess
import pyperclip
from requests import get
from bs4 import BeautifulSoup


def get_title(content):
    try:
        soup = BeautifulSoup(content, feature='lxml')
        return soup.find('title').text.strip()
    except:
        return ''


TMP_FILE = 'article.html'
while os.path.exists(TMP_FILE):
    TMP_FILE = f'article{random.randint(1, 100)}.html'

url = sys.argv[1]
content = get(url).text
STYLESHEET = os.path.expanduser(
    '~/.config/qutebrowser/Dark-stylesheets/0soft.css')
BROWSER = ("surf -a 'a' -b -n -M -s -p -F -C"
           f" {STYLESHEET} "
           "-z 1.5")
title = get_title(content)

try:
    from breadability.readable import Article as reader
    doc = reader(content)
    article = doc.readable
except ImportError:
    from readability import Document
    doc = Document(content)
    article = doc.summary().replace('<html>', '<html><head><title>%s</title></head>' % doc.title())

css_style = ('max-width: 55%; min-width: 20%;'
             'margin:auto; text-align:justify; ;'
             'font-family: bookerly, Serif')
article_format = ('<style>img {max-width: 100%; max-height: 100%;}</style>'
                  f'<div style="{css_style}; font-size:30px">{title}</div>'
                  f'<div id="readabilityBody" style="{css_style}; font-size:20px">')
article = article.replace('<div id="readabilityBody">', article_format)

with codecs.open(TMP_FILE, 'w', 'utf-8') as target:
    target.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    target.write(article)

P = subprocess.Popen(BROWSER.split() + [TMP_FILE])
pyperclip.copy(url)
P.wait()
os.remove(TMP_FILE)
