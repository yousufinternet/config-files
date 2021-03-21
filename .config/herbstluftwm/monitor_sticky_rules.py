#!/usr/bin/env python
import subprocess


def hc(*args):
    P = subprocess.Popen(
        f'herbstclient {" ".join(args)}', text=True, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = not bool(P.stderr.read())
    return P.stdout.read(), err


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


for event in execute('herbstclient --idle'):
    event = event.strip().split()
    # make sticky windows sticky!
    print(event)
    if event[0] == 'rule' and event[1] == 'make_sticky':
        hc(f'chain .-. new_attr bool clients.{event[2]}.my_sticky'
           f' .-. set_attr clients.{event[2]}.my_sticky on')
        
