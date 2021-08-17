#! /usr/bin/env python3
# Heavely inspired by: https://github.com/vimist/lemonbar-manager

import os
import time
import signal
import select
import inspect
import logging
import subprocess
from math import gcd
from functools import reduce

try:
    subprocess.Popen(['killall', 'lemonbar'])
except subprocess.CalledProcessError:
    pass

if os.path.exists('lemonbar.log'):
    os.remove('lemonbar.log')
logging.basicConfig(filename='lemonbar.log', level=logging.DEBUG)

GDKSCALE = int(os.getenv("GDK_SCALE"))


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


script_path = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
os.chdir(script_path)


class MainLoop():
    def __init__(self, modules, logging_level='ERROR',
                 sep=' | ', bg='#000000', fg='#ffffff'):
        logging.info("Intiating Mainloop")
        self.modules = modules
        self.killer = GracefulKiller()
        self.sep = sep
        self.bg, self.fg = bg, fg

    def start_lemonbar(self):
        # TODO arguments to lemonbar should be passed from start script
        self.lemonbar_P = subprocess.Popen(
            (f'lemonbar -p -u {3*GDKSCALE}'
             f' -n lemonbar_python -B "{self.bg}" -F "{self.fg}"'
             # ' -f "TerminessTTF Nerd Font-12:charwidth=14.5"'
             # ' -f "SF Pro Display-10"'
             ' -f "Iosevka-10"'
             f' -f "TerminessTTF Nerd Font-12:charwidth={22.5*GDKSCALE}"'
             # ' -f "FontAwesome"'
             # f' -f "TerminessTTF Nerd Font-12:charwidth={7.25*GDKSCALE}"'
             f' -a 100 -g x{22*GDKSCALE}'),
            text=True, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, encoding='UTF-8')
        logging.debug(
                f'Started lemonbar process {self.lemonbar_P}'
                f' stdout {self.lemonbar_P.stdout}')

    def set_last_update(self, update_time):
        for module in self.modules:
            if not isinstance(module, str):
                setattr(module, 'last_update', update_time)

    def _updaters(self):
        self.updaters = [module.updater for module in self.modules
                         if not isinstance(module, str) and module.updater]
        self.lemonbar_events = self.lemonbar_P.stdout
        self.updaters.append(self.lemonbar_events)
        self.updaters_dict = {
                mod.updater.fileno(): (mod, i)
                for i, mod in enumerate(self.modules)
                if not isinstance(mod, str) and mod.updater}
        self.updaters_dict[self.lemonbar_P.stdout.fileno()] = 'lemonbar'
        self.updaters_poll = select.poll()
        for updater in self.updaters:
            self.updaters_poll.register(updater, 1)

    def _prerequisites(self):
        self.wait_times = [module.wait_time for module in self.modules
                           if not isinstance(module, str)]
        self.wait_times = [wt for wt in self.wait_times if wt != 0]
        logging.info(
                f"Wait times: {', '.join(str(s) for s in self.wait_times)}")
        self._updaters()
        updaters_str = '\n - '.join(str(u) for u in self.updaters)
        logging.info(f"Updaters (on new lines): \n - {updaters_str}")
        logging.info(f"Updaters_dict: {self.updaters_dict}")
        logging.info(' - '+'\n - '.join(f'{mod} : {mod.updater.fileno()}'
                     for mod in self.modules
                     if not isinstance(mod, str) and mod.updater))
        self.outputs = [module.output() if not isinstance(module, str)
                        else module for module in self.modules]
        self.lemonbar_P.stdin.write(' '.join(self.outputs))
        logging.info(f"First outputs to bar: {', '.join(self.outputs)}")

        self.last_loop = 0
        self.end_time = time.time()
        self.ready_updaters = []
        self.set_last_update(self.end_time)

    def start_loop(self):
        self._prerequisites()
        while not self.killer.kill_now:
            self.loop()

    def _wait(self, wait_time):
        start = time.time()
        # used select at first
        self.ready_updaters = self.updaters_poll.poll(wait_time*1000)
        self.ready_updaters = [i[0] for i in self.ready_updaters]
        self.ready_updaters = [upd for upd in self.updaters
                               if upd.fileno() in self.ready_updaters]
        logging.info(f'Waited for {time.time()-start:0.2} Secs')
        logging.info(f'got these ready_updaters: {self.ready_updaters}')

    def _cal_wait(self):
        wait_time = max(0, reduce(gcd, self.wait_times) - self.last_loop)
        # wait_time = min([max(default_wait, wait_time-last_loop)
        #                  for wait_time in wait_times], default=default_wait)
        if self.ready_updaters:
            wait_time = 0
        return wait_time

    def loop(self):
        self.start_time = time.time()
        for i, module in enumerate(self.modules):
            if isinstance(module, str):
                self.outputs[i] = module
                continue
            wait_time = self._cal_wait()
            self._wait(wait_time)
            logging.info(f'Wait time: {float(wait_time):0.2f}')
            logging.info(f'Last loop: {float(self.last_loop):0.2f}')
            logging.info(f'Ready updaters: {self.ready_updaters}')
            logging.debug(f'lemonbar_events: {self.lemonbar_events}')
            if self.ready_updaters:
                for upd in self.ready_updaters:
                    modl = self.updaters_dict[upd.fileno()]
                    if not isinstance(modl, str):
                        logging.info(f'{modl} updater triggered')
                        upd_txt = modl[0].updater.readline().rstrip()
                        print(upd_txt)
                        self.outputs[modl[1]] = modl[0].output()
                        modl[0].last_update = time.time()
                        logging.info(f'{modl} updated successfully')
                    elif modl == 'lemonbar':
                        logging.info('Lemonbar event detected')
                        event = self.lemonbar_events.readline().rstrip()
                        logging.info(f'lemonbar event: {event}')
                        for idx, mod in enumerate(self.modules):
                            if not isinstance(mod, str):
                                update = mod.command(event)
                                if update:
                                    self.outputs[idx] = mod.output()
            if (module.wait_time < self.end_time-module.last_update
                    and module.wait_time != 0):
                logging.info(f'time to update {module}')
                self.outputs[i] = module.output()
                logging.debug(
                        f'{module} output:{self.outputs[i]} to slot:{i}')
                module.last_update = time.time()
            self.write_to_lemonbar()
            self.end_time = time.time()
            self.last_loop = self.end_time - self.start_time

    def write_to_lemonbar(self):
        self.lemonbar_P.stdin.write('\n')
        self.lemonbar_P.stdin.flush()
        self.lemonbar_P.stdin.write(self.sep.join(self.outputs))
