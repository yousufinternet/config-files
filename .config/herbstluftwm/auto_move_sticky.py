#!/usr/bin/env python
# on tag_changed events move sticky windows also
import os
import subprocess as sp


def execute(cmd):
    popen = sp.Popen(cmd, stdout=sp.PIPE,
                     universal_newlines=True, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise sp.CalledProcessError(return_code, cmd)


if __name__ == '__main__':
    for line in execute('herbstclient --idle tag_changed'):
        sp.Popen(os.path.expanduser('~/.config/herbstluftwm/switch_tag.py'),
                shell=True)
