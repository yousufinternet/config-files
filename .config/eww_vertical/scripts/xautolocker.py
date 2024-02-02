#!/usr/bin/env python

import subprocess as sp

coffee = '\uf0f4'
coffee_on = '\uf7b6'
lock = '\uf023'
enabled = eval(sp.getoutput('eww get xautolocker_enabled').strip().title())

def output(self):
    coffee_button = f'(button :onclick `xautolock -{"enable" if enabled else "disable"};xset {"-" if enabled else "+"}dpms;eww update xautolocker_enabled=false` :class "{"grey" if enabled else "green"}-icon" {coffee if enabled else coffee_on})'
    lock = f'(button :onclick `xautolock -locknow` :class "yellow-icon" "{lock}")'

def command(self, event):
    if event == 'XAUTOLOCK':
        # used enable and disable instead of toggle, just incase state has
        # been toggled outside of the bar process, xautolock has no way of
        # querying its current state
        subprocess.Popen(f'xautolock -{"enable" if self.enabled else "disable"}'.split())
        subprocess.Popen(f'xset {"-" if self.enabled else "+"}dpms'.split())
        self.enabled = not self.enabled
        return True
    elif event == 'XAUTOLOCKNOW':
        subprocess.Popen('xautolock -locknow'.split())
