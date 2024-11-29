#!/usr/bin/env python
import sys
import json
import subprocess as sp

P = sp.Popen('hyprctl -j workspaces', text=True, shell=True, stdout=sp.PIPE, encoding='UTF-8')

workspaces_icns = {
    '1': '\uf0ac', '2': '\uf5fc', '3': '\uf120', '4': '\uf02d',
    '5': '\uf1fc', '6': '\uf518', '7': '\uf274',
    '8': '\uf019', '9': '\uf086', '0': '\uf11b'}

icons = True
numbers = False


