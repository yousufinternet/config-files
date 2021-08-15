#!/usr/bin/env bash
if [ $HOSTNAME='yusufs-lenovo' ]
then
    swaymsg input "2:7:SynPS/2_Synaptics_TouchPad" events disabled
    swaymsg input "1:1:AT_Translated_Set_2_keyboard" events disabled
fi

