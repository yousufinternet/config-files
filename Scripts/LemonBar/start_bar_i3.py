#!/usr/bin/env python

from start_lemonbar import create_powerline, lemonbar_below_xfcepanel

from lemonbar_script import MainLoop
from bar_modules import QtileWorkspaces, CoronaVirus, ServerStatus,\
    PingTimeOut, PacmanUpdates, NetworkTraffic, DiskUsage, SARCPUUsage,\
    CPUTemp, RamUsage, Volume, Battery, RandomNum, KeyboardLayout, TimeDate



if __name__ == '__main__':

    bgs = ['#282A36', '#000000']

    modules = [
        QtileWorkspaces(),
        CoronaVirus(),
        ServerStatus('192.168.1.110', 'MC', 22, 'yusuf'),
        PingTimeOut(),
        PacmanUpdates(),
        NetworkTraffic(['lo', 'vboxne']), '%{r}',
        DiskUsage('/home', '\uf015'),
        SARCPUUsage(),
        CPUTemp(),
        RamUsage(),
        Volume(),
        Battery(),
        RandomNum(),
        KeyboardLayout(),
        TimeDate()
    ]

    create_powerline(modules, bgs)

    main_loop = MainLoop(modules, sep='', bg=bgs[0], fg='#F8F8F2')
    main_loop.start_lemonbar()
    lemonbar_below_xfcepanel()
    main_loop.start_loop()
