#!/usr/bin/env python

from start_lemonbar import create_powerline, lemonbar_below_xfcepanel, HOSTNAME

from lemonbar_script import MainLoop
from bar_modules import HerbstluftwmWorkspacesDots, CoronaVirus, ServerStatus,\
    PingTimeOut, PacmanUpdates, NetworkTraffic, DiskUsage, SARCPUUsage,\
    CPUTemp, RamUsage, Volume, Battery, RandomNum, KeyboardLayout, TimeDate,\
    HerbstluftwmWorkspaces, MPC, OpenWeather, UdiskieMenu, SyncthingIndicator, NMInfo


def read_open_weather_api_key():
    with open('OPENWEATHER_APIKEY', 'r') as f: 
        return f.read().strip()


if __name__ == '__main__':

    bgs = ['#282A36', '#000000']

    apikey = read_open_weather_api_key()

    tags_icns = {
        'WEB': '\uf0ac', 'DEV': '\uf5fc', 'TERM': '\uf120', 'DOCS': '\uf02d',
        'GIMP': '\uf1fc', 'READ': '\uf518', 'AGENDA': '\uf274',
        'DOWN': '\uf019', 'CHAT': '\uf086', 'GAME': '\uf11b'}

    if HOSTNAME == 'yusuf-dell':
        modules = [
            HerbstluftwmWorkspaces(tags_icns),
            CoronaVirus(),
            OpenWeather(apikey),
            PacmanUpdates(),
            NetworkTraffic(['lo', 'vboxne']), '%{c}', UdiskieMenu(),
            SyncthingIndicator(), '%{r}',
            SARCPUUsage(),
            CPUTemp(),
            RamUsage(percent=True),
            Volume(),
            Battery(),
            KeyboardLayout(),
            TimeDate()
        ]
    else:
        modules = [
            HerbstluftwmWorkspaces(tags_icns),
            CoronaVirus(),
            OpenWeather(apikey),
            PacmanUpdates(),
            ServerStatus('192.168.1.110', 'MC', 22, 'yusuf'),
            PingTimeOut(),
            NetworkTraffic(['lo', 'vboxne']), '%{c}',
            UdiskieMenu(), SyncthingIndicator(), NMInfo(),
            '%{r}',
            MPC(),
            SARCPUUsage(),
            CPUTemp(),
            RamUsage(percent=True),
            Volume(),
            Battery(),
            KeyboardLayout(),
            TimeDate()
        ]

    # create_powerline(modules, bgs, seps=[' ', ' ', ' ', ' '])

    main_loop = MainLoop(modules, sep='%{F#555555}|%{F-}%{O2}', bg='#000000', fg='#F8F8F2')
    main_loop.start_lemonbar()
    lemonbar_below_xfcepanel()
    main_loop.start_loop()
