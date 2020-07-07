#!/usr/bin/env bash

mpv --force-window=immediate --no-terminal --geometry=1280x720-0-0 --autofit=1280x720 --ytdl-format="bestvideo[height<=?480][fps<=?30]+bestaudio/best" --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched=,cookies="~/Downloads/cookies.txt" $1
