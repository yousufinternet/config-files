import time
import json
import random
import socket
import datetime
import requests
import threading
import subprocess
from bs4 import BeautifulSoup

from colors import dracula as cdict


def cmd_output(cmd, **kwargs):
    try:
        out = subprocess.check_output(cmd, text=True, shell=True).strip()
    except Exception:
        out = ''
    return out


class CoronaVirus():
    'display corona virus cases in iraq'
    def __init__(self):
        self.wait_time = 600  # first time only
        self.updater = None
        self.cache = 'N/A'

    def worldometer_thread(self):
        try:
            page = requests.get(
                    'https://www.worldometers.info/coronavirus/country/iraq/')
            soup = BeautifulSoup(page.content, features='lxml')
            cases = soup.select("div[class='maincounter-number']")
            deaths_recovered = sum(float(c.span.text.replace(',', ''))
                                   for c in cases[1:])
            total_cases = float(cases[0].span.text.replace(',', ''))
            active_cases = total_cases - deaths_recovered
            self.cache = f'{active_cases:0,.0f}'
            if self.wait_time == 600:
                self.wait_time = 1
                time.sleep(2)
                self.wait_time = 6000
        except Exception:
            return

    def output(self):
        T = threading.Thread(target=self.worldometer_thread)
        T.start()
        return ('%{A:CORONA:}%{F'+cdict['green']+'}%{T2}\ue214%'
                '{T-}%{F-}%{O-10}'+self.cache+'%{A}')

    def command(self, event):
        if event.startswith('CORONA'):
            subprocess.Popen(
                'xdg-open https://www.worldometers.info/coronavirus/country/iraq/',
                text=True, shell=True)
            return True


class KeyboardLayout():
    def __init__(self):
        P = subprocess.Popen('xkb-switch -W', text=True, shell=True,
                             stdout=subprocess.PIPE)
        self.updater = P.stdout
        self.wait_time = 60

    def output(self):
        layout = cmd_output('xkb-switch').upper()
        return '%{A:KEYBOARD:}%{T2}\uf80b%{T-}'+layout[0:2]+'%{A}'

    def command(self, event):
        if event == 'KEYBOARD':
            subprocess.Popen('xkb-switch -n', shell=True, text=True)


class PacmanUpdates():
    def __init__(self):
        self.wait_time = 600  # for first update only
        self.updater = None
        self.cache = 'N/A'

    def pacman_thread(self):
        aur_packs = cmd_output('pikaur -Qua | tee /tmp/aurupdates | wc -l')
        official = cmd_output('pacman -Qu | tee /tmp/pacmanupdates | wc -l')
        all = int(aur_packs) + int(official)
        self.cache = all
        if self.wait_time == 600:
            self.wait_time = 1
            time.sleep(1)
            self.wait_time = 3600

    def output(self):
        T = threading.Thread(target=self.pacman_thread)
        T.start()
        return ('%{A:PACMAN:}%{F'+cdict['l_yellow']+'}%{T2}\uf8d6%'
                '{T-}%{F-}%{O-15}'+f'{self.cache}%{{A}}')

    def command(self, event):
        if event.startswith('PACMAN'):
            subprocess.Popen('konsole -e pikaur -Su', text=True, shell=True)


class DiskUsage():
    def __init__(self, mount_point, icon=None):
        self.wait_time = 900
        self.updater = None
        self.mount_point = mount_point
        self.icon = icon

    def output(self):
        df_out = cmd_output('df')
        if df_out:
            used_mnt = [line for line in df_out.split('\n')
                        if line.endswith(self.mount_point)]
            if used_mnt:
                icon = f'%{{T2}}{self.icon}%{{T-}}' if self.icon else ''
                return icon + used_mnt[0].split()[-2]
        return 'N/A'

    def command(self, event):
        pass


class SARCPUUsage():
    def __init__(self):
        self.wait_time = 3
        sar_thread = threading.Thread(target=self.sar_thread)
        sar_thread.start()
        self.updater = None
        self.cache = ""
        self.icon = '\uf0e4'

    def output(self):
        cpu = self.cache
        if cpu.startswith('Linux'):
            return ' '
        elif len(cpu.split('\n')) > 1:
            return ' '
        else:
            cpu_usage = sum(map(float, cpu.split()[3:6]))
            if cpu_usage >= 85:
                return ('%{F'+cdict['red']+'}%{T2}'+self.icon+'%{T-}%{F-}'
                        f'{cpu_usage:0.0f}%')
            else:
                return '%{T2}'+self.icon+'%{T-}'+f'{cpu_usage:0.0f}%'

    def sar_thread(self):
        sar_process = subprocess.Popen(
            f'sar -u {self.wait_time}', text=True, shell=True,
            stdout=subprocess.PIPE)
        for stdout_line in iter(sar_process.stdout.readline, ""):
            self.cache = stdout_line.strip()
        sar_process.stdout.close()
        return_code = sar_process.wait()
        if return_code:
            raise subprocess.CalledProcessError(
                return_code, f'sar -u {self.wait_time}')

    def command(self, event):
        pass


class NetworkTraffic():
    def __init__(self, exclude=['lo']):
        self.wait_time = 5
        self.updater = None
        self.cache = []
        self.exclude = exclude

    def get_ip_out(self):
        'parse the json output of ip command'
        iface = cmd_output('ip -s -j link')
        ifaces = [
            (d['ifname'],
             d['stats64']['rx']['bytes']/1000,
             d['stats64']['tx']['bytes']/1000)
            for d in json.loads(iface)
            if not any(x in d['ifname'] for x in self.exclude)
            and 'UP' in d['flags']]
        return ifaces

    def output(self):
        'lemonbar ready output'
        updt = self.wait_time
        ifaces = self.get_ip_out()
        iftxt_len = 3
        if len(ifaces) == len(self.cache):
            speeds = [
                (ifaces[i][0] if len(ifaces[i][0]) < iftxt_len
                 else ifaces[i][0][:iftxt_len],
                 round((ifaces[i][1]-self.cache[i][1])/updt),
                 round((ifaces[i][2]-self.cache[i][2])/updt))
                for i in range(len(ifaces))]
        else:
            speeds = [
                (ifaces[i][0] if len(ifaces[i][0]) < iftxt_len
                 else ifaces[i][0][:iftxt_len],
                 0, 0) for i in range(len(ifaces))]
        formated_speeds = '/ '.join(
            (f'%{{F{cdict["teal"]}}}{x[0].upper()}%{{F-}} '
             f'{x[2]} %{{F{cdict["orange"]}}}%{{T2}}\uf55c%{{T-}}%{{F-}}%{{O-10}}'
             f'{x[1]} %{{F{cdict["green"]}}}%{{T2}}\uf544%{{T-}}%{{F-}}%{{O-15}}')
            for x in speeds)
        self.cache = self.get_ip_out()
        return formated_speeds

    def command(self, event): pass


class PingTimeOut():
    'constantly listen to ping and output the ping time'
    def __init__(self, remote_server='archlinux.org'):
        self.wait_time = 30
        ping_thread = threading.Thread(target=self.ping_thread,
                                       args=[remote_server])
        ping_thread.start()
        self.updater = None
        self.ping_cache = ""
        self.previous_ping = ""

    def output(self):
        ping_time = self.ping_cache if not self.ping_cache == self.previous_ping else ""
        self.previous_ping = self.ping_cache
        try:
            return ('%{F'+cdict['green']+'}%{T2}\uf0ac%{T-}%{F-}'
                    f'{ping_time.split()[-2].split("=")[1]} ms')
        except IndexError:
            return '%{F'+cdict['red']+'}%{T2}\uf0ac%{T-}%{F-}'

    def ping_thread(self, remote_server):
        ping_process = subprocess.Popen(
            f'ping -i 30 -W 1 {remote_server}', text=True, shell=True,
            stdout=subprocess.PIPE)
        for stdout_line in iter(ping_process.stdout.readline, ""):
            self.ping_cache = stdout_line.strip()
        ping_process.stdout.close()
        return_code = ping_process.wait()
        if return_code:
            raise subprocess.CalledProcessError(
                return_code, 'ping -i 30 -W 1 archlinux.org')

    def command(self, event):
        pass


class CPUTemp():
    def __init__(self):
        self.wait_time = 10
        self.updater = None
        self.icons_dict = {50: '\uf2cb', 60: '\uf2ca', 70: '\uf2c9',
                           80: '\uf2c8', 90: '\uf2c7'}

    def output(self):
        sensors = cmd_output('sensors')
        temps = [int(line.split()[2].split('.')[0]) for line in
                 sensors.split('\n') if line.startswith('Core')]
        avg_temp = sum(temps)/len(temps)
        icon = [v for k, v in self.icons_dict.items() if k >= avg_temp or k == 90][0]
        if avg_temp > 80:
            return '%{F'+cdict['red']+'}%{T2}'+icon+'%{T-}%{O-15}'+str(round(avg_temp))+'%{F-}'
        else:
            return '%{T2}'+icon+'%{T-}%{O-15}'+str(round(avg_temp))

    def command(self, event):
        pass


class CPUUsage():
    def __init__(self):
        self.wait_time = 1
        self.updater = None
        self.icon = '\uf0e4'

    def output(self):
        cpu_usage = sum(float(i) for i in cmd_output(
            'mpstat -P ALL').split('\n')[3].split()[3:6])
        if cpu_usage >= 85:
            return ('%{F'+cdict['red']+'}%{T2}'+self.icon+'%{T-}'
                    f'{cpu_usage:0.1f}%{{F-}}')
        else:
            return ('%{T2}'+self.icon+'%{T-}'
                    f'{cpu_usage:0.1f}%')

    def command(self, event):
        pass


class RamUsage():
    def __init__(self):
        self.wait_time = 30
        self.updater = None
        self.icon = '\ue266'

    def output(self):
        ram = cmd_output('vmstat -s').split('\n')
        used = int(ram[1].strip().split()[0])/(1024**2)
        total = int(ram[0].strip().split()[0])/(1024**2)
        if used/total > 0.85:
            return ('%{F'+cdict['red']+'}%{T2}'
                    f'{self.icon}%{{T-}}{used:0.1f}G/{total:0.1f}G'+'%{F-}')
        else:
            return f'%{{F{cdict["green"]}}}%{{T2}}{self.icon}%{{T-}}%{{F-}}{used:0.1f}G/{total:0.1f}G'

    def command(self, event):
        pass


class CurrentWindow():
    # TODO
    def __init__(self):
        P = subprocess.Popen('bspc subscribe', text=True, shell=True,
                             stdout=subprocess.PIPE, encoding='UTF-8')
        self.updater = P.stdout
        self.wait_time = 60

    def output(self):
        win_title = cmd_output('bspc query -N -n | xtitle')
        win_title = win_title+' '*(28-len(win_title)) if len(win_title) < 28 else win_title[:25]+'...'
        return win_title

    def command(self, event):
        pass


class ServerStatus():
    # TODO: send wake on lan upon click
    def __init__(self, server_ip, server_alias, server_port=22, server_user=None):
        self.wait_time = 300
        self.updater = None
        self.server_ip = server_ip
        self.server_alias = server_alias
        self.server_user = server_user
        self.server_port = server_port
        self.successful = False

    def sock_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server_ip, self.server_port))
            self.successful = True
        except socket.error:
            self.successful = False
            sock.close()

    def output(self):
        sock_thread = threading.Thread(target=self.sock_thread)
        sock_thread.start()
        if self.server_user and self.successful:
            return ('%{A:SSH'+self.server_alias+':}'
                    f'%{{F{cdict["green"]}}}' +
                    self.server_alias+'%{F-}%{A}')
        if self.successful:
            return '%{F'+cdict['green']+'}'+self.server_alias+'%{F-}'
        return '%{F'+cdict['red']+'}'+self.server_alias+'%{F-}'

    def command(self, event):
        if event.startswith(f'SSH{self.server_alias}'):
            subprocess.Popen('konsole -e ssh '+self.server_user+'@'+self.server_ip,
                             text=True, shell=True)


class Battery():
    def __init__(self):
        self.wait_time = 60
        self.updater = None
        self.icons = {5: '\uf244', 25: '\uf243', 50: '\uf242',
                      75: '\uf241', 100: '\uf240'}

    def output(self):
        battery = cmd_output('acpi --battery')
        if battery != '':
            battery = battery.split(': ')[1].split(', ')[1]
            bat_vlu = int(battery.rstrip('%'))
            icon = [v for k, v in self.icons.items() if k >= bat_vlu][0]
            if bat_vlu <= 5:
                return f'%{{B{cdict["red"]}}}%{{T2}}{icon} %{{T-}}'+battery+'%{B-}'
            elif bat_vlu == 100:
                return f'%{{F{cdict["green"]}}}%{{T2}}{icon} %{{T-}}'+battery+'%{F-}'
            else:
                return f'%{{T2}}{icon} %{{T-}}'+battery

    def command(self, event):
        pass


class BspwmWorkspaces():
    def __init__(self):
        P = subprocess.Popen('bspc subscribe', text=True, shell=True,
                             stdout=subprocess.PIPE, encoding='UTF-8')
        self.updater = P.stdout
        self.wait_time = 60

    def output(self):
        all_workspaces = cmd_output(
            'bspc query -D --names').strip().split('\n')
        just_len = len(max(all_workspaces, key=len))
        empty_workspaces = []
        for desk in all_workspaces:
            wins = cmd_output(f"bspc query -N -d {desk}")
            wins = [] if wins == '' else wins
            if len(wins) == 0:
                empty_workspaces.append(desk)
        current = cmd_output('bspc query -D -d --names').strip()
        try:
            urgent = cmd_output(
                    'bspc query -D -d .urgent --names').strip().split('\n')
        except subprocess.CalledProcessError:
            urgent = []

        pre1 = '%{A:BSPWM_WIDGETdesk'
        pre2 = '%{A4:BSPWM_WIDGETnext:}'
        pre3 = '%{A5:BSPWM_WIDGETprev:}'
        formatted_ws = []
        for w in all_workspaces:
            # wor = f' {w} '
            wor = '%{T3}'+w.center(just_len+2)+'%{T1}'
            if w == current:
                formatted_ws.append('%{R}'+wor+'%{R}')
            elif w in urgent:
                formatted_ws.append(
                    pre1+w+':}'+'%{U'+cdict['red']+'}%{+o}'+wor+'%{-o}%{U-}%{A}')
            elif w in empty_workspaces:
                formatted_ws.append(
                    pre1+w+':}'+'%{U'+cdict['cyan']+'}%{+o}'+wor+'%{-o}%{U-}%{A}')
            else:
                formatted_ws.append(
                    pre1+w+':}'+wor+'%{A}')

        return pre2+pre3+''.join(formatted_ws)+'%{A5}%{A4}'

    def command(self, event):
        if event.startswith('BSPWM_WIDGETdesk'):
            w = event.strip()[16:]
            print(w)
            subprocess.Popen(f'bspc desktop -f {w}', text=True, shell=True)
        elif event in ['BSPWM_WIDGETnext', 'BSPWM_WIDGETprev']:
            subprocess.Popen(f'bspc desktop -f {event[-4:]}',
                             text=True, shell=True)


class Volume():
    def __init__(self):
        self.wait_time = 4
        self.updater = None
        self.icons = {0: '\uf466', 25: '\uf027', 100: '\uf028'}

    def output(self):
        vol = cmd_output('pamixer --get-volume')
        vol = vol if vol != '' else '0'
        prefix = ('%{A3:pactl set-sink-volume @DEFAULT_SINK@ 100%:}%{A:pactl'
                  ' set-sink-volume @DEFAULT_SINK@ 0:}%{A4:pactl set'
                  '-sink-volume @DEFAULT_SINK@ +2%:}%{A5:pactl set-sink-volume'
                  ' @DEFAULT_SINK@ -2%:}')

        icon = [v for k, v in self.icons.items()
                if k >= int(vol) or k == 100][0]
        suffix = '%{A5}%{A4}%{A}%{A3}'
        return prefix+f'%{{T2}}{icon}%{{T-}}{int(vol):02d}%'+suffix

    def command(self, event):
        if event.startswith('pactl'):
            subprocess.Popen(event, text=True, shell=True)
        return True


class TimeDate():
    def __init__(self):
        self.wait_time = 1
        self.updater = None

    def output(self):
        clock_faces = {(0, 0): "🕛", (1, 0): "🕐", (2, 0): "🕑",
                       (3, 0): "🕒", (4, 0): "🕓", (5, 0): "🕔",
                       (6, 0): "🕕", (7, 0): "🕖", (8, 0): "🕗",
                       (9, 0): "🕘", (10, 0): "🕙", (11, 0): "🕚",
                       (0, 30): "🕧", (1, 30): "🕜", (2, 30): "🕝",
                       (3, 30): "🕞", (4, 30): "🕟", (5, 30): "🕠",
                       (6, 30): "🕡", (7, 30): "🕢", (8, 30): "🕣",
                       (9, 30): "🕤", (10, 30): "🕥", (11, 30): "🕦"}
        clock_faces = {0: '\ue381', 1: '\ue382', 2: '\ue383', 3: '\ue384', 4: '\ue385',
                      5: '\ue386', 6: '\ue387', 7: '\ue388', 8: '\ue389', 9: '\ue38a',
                      10: '\ue38b', 11: '\ue38c'}
        now = datetime.datetime.now()
        current_face = now.hour if now.hour < 12 else now.hour-12
        # 0 if now.minute < 30 else 30)
        date_time = datetime.datetime.strftime(
            now, '%{T2}%{F'+cdict['l_yellow']+'}\uf073 %{F-}%{T1}%{O-15}%a %Y-%m-%d %H:%M:%S')
        return date_time+'%{T2} '+clock_faces[current_face]+'%{T-}%{O-15}'

    def command(self, event):
        print(event)


class RandomNum():
    def __init__(self):
        self.wait_time = 60
        self.updater = None
        self.event = 'Update Num'

    def output(self):
        num = random.randint(0, 100)
        color = cdict['green'] if num == 100 else '-'
        return f'%{{A:Update Num:}}%{{F{color}}}' + str(num)+'%{F-}%{A}'

    def command(self, event):
        if event == 'Update Num':
            return True
