#!/bin/bash

# if [ $GDK_SCALE = 2 ]; then
#     hybrid="optirun"
# else
#     hybrid=""
# fi

# bumblebee_installed=$(pacman -Qe bumblebee| wc -l)
# if [ $bumblebee_installed = 1 ]; then
# '-n' means the string is not of zero length
if [ -n "$(pacman -Qe bumblebee 2> /dev/null | wc -l)" ]; then
    hybrid="optirun"
fi

echo $hybrid $@
exec $hybrid $@ &

exit
