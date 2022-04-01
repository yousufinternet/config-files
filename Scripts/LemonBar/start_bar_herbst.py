#!/usr/bin/env python

import sys
from start_lemonbar import create_powerline, lemonbar_below_xfcepanel, HOSTNAME

from colors import modus_vivendi as cdict
from lemonbar_script import MainLoop
from bar_modules import HerbstluftwmWorkspacesDots, CoronaVirus, ServerStatus,\
    PingTimeOut, PacmanUpdates, NetworkTraffic, DiskUsage, SARCPUUsage,\
    CPUTemp, RamUsage, Volume, Battery, RandomNum, KeyboardLayout, TimeDate,\
    HerbstluftwmWorkspaces, MPC, OpenWeather, UdiskieMenu, SyncthingIndicator,\
    NMInfo, ficon, PodsBuddy, XAutoLocker, DarkLightSwitcher


def read_open_weather_api_key():
    with open('OPENWEATHER_APIKEY', 'r') as f_obj:
        return f_obj.read().strip()


if __name__ == '__main__':

    bgs = ['#282A36', '#000000', '#373844', '#1E2029', '#6272a4']

    apikey = read_open_weather_api_key()

    tags_icns = {
        'WEB': '\uf0ac', 'DEV': '\uf5fc', 'TERM': '\uf120', 'DOCS': '\uf02d',
        'GIMP': '\uf1fc', 'READ': '\uf518', 'AGENDA': '\uf274',
        'DOWN': '\uf019', 'CHAT': '\uf086', 'GAME': '\uf11b'}

    if HOSTNAME == 'yusufs-dell':
        modules = [
            '%{Sl}' if len(sys.argv) < 2 else '%{S'+sys.argv[1]+'}',
            HerbstluftwmWorkspaces(tags_icns),
            OpenWeather(apikey),
            PacmanUpdates(),
            NetworkTraffic(['lo', 'vboxne']), '%{c}', UdiskieMenu(),
            SyncthingIndicator(), NMInfo(), PodsBuddy(), XAutoLocker(),
            '%{r}',
            SARCPUUsage(),
            Volume(),
            Battery(),
            DarkLightSwitcher(),
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
            PodsBuddy(), XAutoLocker(),
            MPC(),
            '%{r}',
            SARCPUUsage(), CPUTemp(),
            RamUsage(percent=True),
            Volume(),
            Battery(),
            KeyboardLayout(),
            TimeDate()
        ]

    # seps = [ficon('\ue0b0'), ficon('\ue0b1', beforepad=5), ficon('\ue0b2', afterpad=-0.5),
    #         ficon('\ue0b3', beforepad=5)]
    # seps = [' ', ficon('\ue0b1', beforepad=5), ' ', ficon('\ue0b3', beforepad=5)]
    # create_powerline(modules, bgs, seps=seps)

    # main_loop = MainLoop(modules, sep='', bg='#282a36', fg='#F8F8F2')
    main_loop = MainLoop(
        modules,
        sep='%{O5}%{F'+cdict['dimmed']+'}/%{F-}%{O5}',
        bg=cdict['background'],
        fg=cdict['foreground'])
    main_loop.start_lemonbar()
    lemonbar_below_xfcepanel()
    main_loop.start_loop()
