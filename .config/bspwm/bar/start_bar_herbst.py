#!/usr/bin/env python

from start_lemonbar import create_powerline, lemonbar_below_xfcepanel, HOSTNAME

from lemonbar_script import MainLoop
from bar_modules import HerbstluftwmWorkspacesDots, CoronaVirus, ServerStatus,\
    PingTimeOut, PacmanUpdates, NetworkTraffic, DiskUsage, SARCPUUsage,\
    CPUTemp, RamUsage, Volume, Battery, RandomNum, KeyboardLayout, TimeDate


if __name__ == '__main__':

    bgs = ['#282A36', '#000000']

    if HOSTNAME == 'yusuf-dell':
        modules = [
            HerbstluftwmWorkspacesDots(),
            CoronaVirus(),
            PacmanUpdates(),
            NetworkTraffic(['lo', 'vboxne']), '%{r}',
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
            HerbstluftwmWorkspacesDots(),
            CoronaVirus(),
            PacmanUpdates(),
            ServerStatus('192.168.1.110', 'MC', 22, 'yusuf'),
            PingTimeOut(),
            NetworkTraffic(['lo', 'vboxne']), '%{r}',
            SARCPUUsage(),
            CPUTemp(),
            RamUsage(percent=True),
            Volume(),
            Battery(),
            KeyboardLayout(),
            TimeDate()
        ]

    create_powerline(modules, bgs)

    main_loop = MainLoop(modules, sep='', bg=bgs[0], fg='#F8F8F2')
    main_loop.start_lemonbar()
    lemonbar_below_xfcepanel()
    main_loop.start_loop()
