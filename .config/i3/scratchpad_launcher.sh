#!/bin/bash

open_scratchs=$(wmctrl -lx | grep -Ei "$1.*$2.*" | wc -l)

if [[ open_scratchs -eq 0 ]]; then
   i3-msg "exec $3"
fi

i3-msg "[title=\"$2\"] scratchpad show"
