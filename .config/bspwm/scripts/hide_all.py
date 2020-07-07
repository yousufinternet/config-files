#! /usr/bin/env python3
from wmutils.processes import cmd_run, cmd_output


def hideall():
    for win in cmd_output(
            "bspc query -N -d -n '.!hidden.window.!focused'").split('\n'):
        cmd_run(f'bspc node {win} -g hidden=on')


if __name__ == '__main__':
    hideall()
