#!/usr/bin/env python
import sys
import subprocess as sp

playback_monitor = sp.Popen('playerctl -F status', shell=True, text=True, stdout=sp.PIPE)

def output():
    media_players = sp.getoutput('playerctl -l').splitlines()
    enclosure = '(box :space-evenly false :orientation "v" :spacing 10 {})'
    player_enclosure = '(eventbox :onhover `${{EWW_CMD}} update player_{idx}_reveal=true` :onhoverlost `${{EWW_CMD}} update player_{idx}_reveal=false` (box :space-evenly false :orientation "v" :spacing 5 {player}))'
    item_label = '(eventbox :onclick `playerctl -p {playername} {action}` (label :tooltip "{title} | {artist}" :class "icon" :text "{icon}"))'
    generic_icon = '(eventbox :onclick `playerctl -p {playername} {action}` (label :tooltip "{tooltip}" :class "icon" :text "{icon}"))'
    players_list = []
    top_revealer = '(revealer :reveal player_{idx}_reveal :transition "slideup" {widget})'
    bottom_revealer = '(revealer :reveal player_{idx}_reveal :transition "slidedown" (box :orientation "v" :space-evenly false :spacing 5 {widget}))'

    for idx, media_player in enumerate(media_players):
        prev_track = generic_icon.format(
            action="previous", playername=media_player, tooltip="Previous", icon="\uf048")
        next_track = generic_icon.format(
            action="next", tooltip="Next", playername=media_player, icon="\uf051")
        stop = generic_icon.format(
            action="stop", playername=media_player, tooltip="Stop", icon="\uf28d")
        status = sp.getoutput(f'playerctl -p {media_player} status')
        if status == 'Playing':
            title, artist = sp.getoutput(f'playerctl -p {media_player} metadata --format '+"'{{title}}\n{{artist}}'").splitlines()
        else:
            title, artist = '', ''
        icon = '\uf28b' if status == 'Playing' else '\uf144'
        play_pause = item_label.format(idx=idx, playername=media_player, title=title, artist=artist, icon=icon, action='pause' if status=='Playing' else 'play')
        top_rev = top_revealer.format(idx=idx, widget=prev_track)
        bot_rev = bottom_revealer.format(idx=idx, widget=' '.join([stop, next_track]))
        players_list.append(player_enclosure.format(idx=idx, player=' '.join([top_rev, play_pause, bot_rev])))
    return enclosure.format(' '.join(players_list))

    
while True:
    out = output()
    print(out)
    sys.stdout.flush()
    playback_monitor.stdout.readline()

