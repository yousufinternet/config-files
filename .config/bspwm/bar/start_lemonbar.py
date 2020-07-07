#! /usr/bin/env python3

import time
import random
import subprocess
from itertools import permutations

from lemonbar_script import MainLoop
from bar_modules import BspwmWorkspaces, CoronaVirus, ServerStatus,\
    PingTimeOut, PacmanUpdates, NetworkTraffic, DiskUsage, SARCPUUsage,\
    CPUTemp, RamUsage, Volume, Battery, RandomNum, KeyboardLayout, TimeDate



# bgs = ['#282828', '#504945', '#1d2021', '#3c3836']
bgs = ['#282A36', '#000000']

seps = [
    '%{T2}\uE0B0%{O-27}%{T-}', '%{F#F8F8F2}%{T2} \uE0B1%{T-}%{F-}',
    '%{T2}\uE0B2%{O-28}%{T-}', '%{F#F8F8F2}%{T2} \uE0B3%{T-}%{F-}'
]

# seps = [' %{O-5}',]*4
# seps = [
#     '%{T2}\uE0BC%{T-}', '%{F#a89984}%{T2} \uE0BB%{T-}%{F-}',
#     '%{T2}\uE0BE%{T-}', '%{F#a89984}%{T2} \uE0B9%{T-}%{F-}'
# ]


def generate_powerline(bgs, sep, flipped):
    '''
    add colors and formatting to the passed separator
    '''
    # TODO wrap powerline funcs in a class and
    # integrate them with the main code
    bg, fg = bgs
    if flipped:
        return f'%{{O10}}%{{F{bg}}}%{{B{fg}}}' f'{sep}%{{F-}}%{{B{bg}}} '
    return f'%{{O10}}%{{F{fg}}}%{{B{bg}}}' f'{sep}%{{O10}}%{{F-}}'


def new_pair(perms, fg=None, bg=None):
    if bg and fg:
        return [b for b in perms if b == (bg, fg)][0]
    if bg:
        return random.choice([b for b in perms if b[0] == bg])
    return random.choice([b for b in perms if b[1] == fg])


def create_powerline(modules, bgs):
    bgs_perm = list(permutations(bgs, 2))
    last_bgs = new_pair(bgs_perm, fg=bgs[0])
    modules_len = len(modules)
    flipped_flag = False
    sep, silent_sep = seps[0], seps[1]
    powerline = generate_powerline(last_bgs, sep, flipped_flag)
    for idx in range(modules_len):
        i = idx * 2 + 1  # index in modules after insertion
        if i >= len(modules):
            break
        mod = modules[i]
        next_mod = (modules[i+1:i+2] or (modules[-1],))[0]
        print(mod, next_mod)
        if mod == '%{r}':
            modules[i] = '%{F-}%{B-}%{r}'
            flipped_flag = True
            sep, silent_sep = seps[2], seps[3]
        if (idx+1) % 3 == 0 and '%{r}' not in [mod, next_mod]:
            modules.insert(i, silent_sep)
            continue
        modules.insert(i, powerline)
        # when specifying colors for the next module see if the one after it is
        # %{r} and choose a one with the default background if so
        if next_mod == '%{r}':
            if bgs[0] == last_bgs[0]:
                powerline = seps[1]
                continue
            last_bgs = new_pair(bgs_perm, bg=bgs[0], fg=last_bgs[0])
            last_bgs = ('-', last_bgs[1])
        else:
            last_bgs = new_pair(
                bgs_perm, fg=bgs[0] if last_bgs[0] == '-' else last_bgs[0])
        powerline = generate_powerline(last_bgs, sep, flipped_flag)
    modules.insert(0, '%{B-}')


def lemonbar_below_xfcepanel():
    '''
    Put lemonbar below xfce4-panel
    '''
    try:
        time.sleep(0.1)
        xfce_ids = subprocess.check_output(
            'xdo id -a xfce4-panel', text=True, shell=True).strip().split('\n')
        for i in xfce_ids:
            subprocess.Popen(
                f'xdo below -t {i} -a lemonbar_python', text=True, shell=True)
    except subprocess.CalledProcessError:
        pass


if __name__ == '__main__':
    modules = [
        BspwmWorkspaces(),
        CoronaVirus(),
        ServerStatus('192.168.1.109', 'MC', 22, 'yusuf'),
        PingTimeOut(),
        PacmanUpdates(),
        NetworkTraffic(['lo', 'enp9s0', 'vboxne']), '%{r}',
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
