import subprocess
from functools import partial

cmd_run = partial(subprocess.Popen, text=True, shell=True)


def is_child(pid, child_pid):
    '''
    check whether child_pid is a child of pid
    '''
    tree = cmd_output(f'pstree -T -p {pid}')
    for line in tree.split('\n'):
        if child_pid in line:
            return True
    return False


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def cmd_output(cmd):
    '''
    subprocess's check output with some defaults and exception handling
    '''
    try:
        out = subprocess.check_output(cmd, text=True, shell=True).strip()
    except Exception:
        out = ''
    return out

