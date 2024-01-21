#!/usr/bin/env bash

xprop -id `xdotool getwindowfocus` | grep '_NET_WM_PID' | grep -oE '[[:digit:]]*$'
qdbus org.pwmt.zathura.PID-1032817 /org/pwmt/zathura org.pwmt.zathura.pagenumber
qdbus org.pwmt.zathura.PID-1032817 /org/pwmt/zathura org.pwmt.zathura.filename
