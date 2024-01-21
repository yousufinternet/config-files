#!/usr/bin/env bash

cat ~/Scripts/RofiMenus/oil_industry_abbreviations | rofi -matching regex -i -filter "^" -dmenu
