#!/usr/bin/env python

import os
import sys
import time
import sched
import inspect
import datetime
from wmutils.processes import cmd_run

WAL_PATH = os.path.join(os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))), 'wal_path')


def wal_full_path(wal_dir, wal_ext, wal_name, wal_num):
    return os.path.join(wal_dir, f'{wal_name}_{wal_num}.{wal_ext}')


def dynamic_wallpaper(wal_dir):
    wals = os.listdir(wal_dir)
    wal_ext = wals[0].split('.')[-1]
    wal_name = '_'.join('.'.join(wals[0].split('.')[:-1]).split('_')[:-1])
    mins_per_wal = round(1440 / len(wals))  # 1440 minutes per 24 hours
    now = datetime.datetime.now()
    mins_since_0 = now.hour*60 + now.minute
    start_wal_no = (mins_since_0 // mins_per_wal) + 1
    wal_path = wal_full_path(wal_dir, wal_ext, wal_name, start_wal_no)
    print(wal_path)
    set_single_wallpaper(wal_path)
    s = setup_scheduler()
    while True:
        for i in range(1, len(wals)+1):
            wait_time = (i if i > start_wal_no else i+len(wals))
            wait_time = (wait_time-1)*mins_per_wal - mins_since_0
            wal_path = wal_full_path(wal_dir, wal_ext, wal_name, i)
            s.enter(wait_time*60, 1, set_single_wallpaper, argument=(wal_path,))
        s.run()


def setup_scheduler():
    return sched.scheduler(time.time, time.sleep)


def set_single_wallpaper(path):
    cmd_run(f'feh --bg-fill "{path}"')
    # cmd_run(f'wal -s -i "{path}"')


def set_wal(path):
    if os.path.isdir(path):
        dynamic_wallpaper(path)
    else:
        set_single_wallpaper(path)


def store_wal_path(wal_path):
    with open(WAL_PATH, 'w+') as f_obj:
        f_obj.write(wal_path)


def read_stored_wal():
    if os.path.exists(WAL_PATH):
        with open(WAL_PATH) as f_obj:
            return f_obj.read().strip()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        wal_path = read_stored_wal()
    else:
        wal_path = os.path.abspath(sys.argv[1])
        store_wal_path(wal_path)
    set_wal(wal_path)
