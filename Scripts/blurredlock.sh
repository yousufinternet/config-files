#!/usr/bin/env bash

scrot -o ~/.cache/screenshot.png
convert ~/.cache/screenshot.png -blur 0x10 ~/.cache/screenshot.png
i3lock -n -f -e -i ~/.cache/screenshot.png
