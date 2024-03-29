import os
import time
import json
import random
import socket
import calendar
import datetime
import requests
import threading
import subprocess
from io import StringIO
from bs4 import BeautifulSoup

from colors import modus_vivendi as cdict

from lemonbar_script import GDKSCALE


def cmd_output(cmd, **kwargs):
    try:
        out = subprocess.check_output(cmd, text=True, shell=True).strip()
    except Exception:
        out = ''
    return out


def ficon(icon, color=None, beforepad=0, afterpad=5, idx=2, swap=False):
    '''
    idx: index of font to be used
    '''
    beforepad *= GDKSCALE
    afterpad *= GDKSCALE
    return ('%{O'+f'{beforepad}'+'}'+('%{F'+color+'}' if color else '')+
            ('%{R}' if swap else '')+'%{T'+
            f'{idx}'+'}' + icon+'%{T-}'+('%{R}' if swap else '')+('%{F-}' if color else '')+'%{O'+
            f'{afterpad}'+'}')


def read_fwf(text_table):
    """
    only works when the first row is columns with a single word
    """
    cols_row = text_table.splitlines()[0]
    columns = cols_row.split()
    cols_idxs = []
    for i, (col, colnxt) in enumerate(zip(columns, columns[1:])):
        cols_idxs.append((0 if i == 0 else cols_row.index(f' {col}')+1,
                     cols_row.index(f' {colnxt}')+1))
    # cols_widths = [(cols_row.index(c), cols_row.index(cnxt)) for c, cnxt in zip(columns, columns[1:])]
    cols_idxs.append((cols_row.index(f' {columns[-1]}')+1, -1))
    final_dict = {
        col: [l[col_idx[0] : col_idx[1]].strip() for l in
              text_table.splitlines()[1:]]
        for col, col_idx in zip(columns, cols_idxs)
    }
    return final_dict


class MPC():
    def __init__(self, wait_time=30):
        self.wait_time = wait_time
        P = subprocess.Popen('mpc idleloop', text=True, shell=True,
                             stdout=subprocess.PIPE)
        self.updater = P.stdout
        self.icons_dict = {'stop': '\uf04d', 'playing': '\uf04b', 'paused': '\uf04c'}

    def output(self):
        try:
            song = subprocess.check_output('mpc current', text=True, shell=True).splitlines()[0]
            mpc_state = subprocess.check_output('mpc', text=True, shell=True).splitlines()
            if len(mpc_state) == 1:
                state = 'stop'
            else:
                state = mpc_state[1].split()[0][1:-1]
            if len(song) > 40:
                song = song[:39]+'…'
        except (subprocess.CalledProcessError, IndexError):
            state = 'stop'
            song = ''
        icon = ficon(self.icons_dict[state], cdict['l_yellow'])
        return '%{A4:mpcnext:}%{A5:mpcprev:}%{A:mpctoggle:}%{A3:mpcstop:}'+icon+song+'%{A3}%{A}%{A5}%{A4}'

    def command(self, event):
        if event.startswith('mpc'):
            subprocess.run(f'mpc {event[3:]}', text=True, shell=True)
            return True


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
        return ('%{A:CORONA:}'+ficon('\ue076', cdict['green'])+self.cache+'%{A}')

    def command(self, event):
        if event.startswith('CORONA'):
            subprocess.Popen(
                'xdg-open https://www.worldometers.info/coronavirus/country/iraq/',
                text=True, shell=True)
            return True


class OpenWeather():
    'display corona virus cases in iraq'
    def __init__(self, apikey, lat=30.5349, lon=47.7888):
        self.wait_time = 600  # first time only
        self.updater = None
        self.lat, self.lon = lat, lon
        self.APIkey = apikey
        self.cache = 'N/A'
        self.icons = {
            'DEFAULT': '\uf185', '01d': '\uf185', '01n': '\uf186', '02d': '\uf6c4',
            '02n': '\uf6c3', '03d': '\uf0c2', '03n': '\uf0c2', '04d': '\uf0c2',
            '04n': '\uf0c2', '09d': '\uf740', '09n': '\uf740', '10d': '\uf743',
            '10n': '\uf73c', '11d': '\uf0e7', '11n': '\uf0e7', '12d': '\uf2dc',
            '12n': '\uf2dc', '50d': '\uf72e', '50n': '\uf72e'}

    def openweather_thread(self):
        try:
            req_link = f"https://api.openweathermap.org/data/2.5/onecall?lat={self.lat}&lon={self.lon}&exclude=minutely,hourly,alerts&appid={self.APIkey}&units=metric"
            # req_link = f'http://api.openweathermap.org/data/2.5/weather?q={self.city_name}&units=metric&appid={self.APIkey}'
            response = requests.get(req_link)
            if response:
                self.cache = response.json()
            if self.wait_time == 600:
                self.wait_time = 1
                time.sleep(4)
                self.wait_time = 600
        except Exception:
            return

    def output(self):
        if self.APIkey:
            T = threading.Thread(target=self.openweather_thread)
            T.start()
        if isinstance(self.cache, dict):
            icon = self.icons.get(self.cache['current']['weather'][0]['icon'],
                                  self.icons['DEFAULT'])
            temp = f'{self.cache["current"]["temp"]:0.0f} ℃'
            return ("%{A:OPENWEATHER:}"+ficon(icon, cdict['l_yellow'])+temp+"%{A}")
        return '%{A:OPENWEATHER:}'+ficon(self.icons['DEFAULT'], cdict['l_yellow'])+self.cache+'%{A}'

    def format_notification(self):
        temp_keys = ["min", "max", "morn", "eve", "night"]
        if isinstance(self.cache, dict):
            return (
                "DATE    | MIN | MAX | MOR | EVE | NGT |\n" + "\n".join(
                    datetime.datetime.fromtimestamp(dfr["dt"]).strftime("%d-%m %a ")
                    + " ".join(f'{dfr["temp"][k]: ^5.0f}' for k in temp_keys)
                    for dfr in self.cache["daily"]))
        return "SERVICE NOT AVAILABLE"

    def command(self, event):
        if event.startswith('OPENWEATHER'):
            content = self.format_notification()
            subprocess.Popen(
                ('dunstify -i "noicon" -a " " -t 60000'
                 f' "Weather Forecast" "{content}"'), shell=True, text=True)
            return True


class KeyboardLayout():
    def __init__(self):
        P = subprocess.Popen('xkb-switch -W', text=True, shell=True,
                             stdout=subprocess.PIPE)
        self.updater = P.stdout
        self.wait_time = 600

    def output(self):
        layout = cmd_output('xkb-switch').upper()
        return '%{A:KEYBOARD:}'+ficon('\uf11c')+layout[0:2]+'%{A}'

    def command(self, event):
        if event == 'KEYBOARD':
            subprocess.Popen('xkb-switch -n', shell=True, text=True)


class NMInfo():
    def __init__(self, exclude=[]):
        P = subprocess.Popen('nmcli monitor', text=True, shell=True,
                             stdout=subprocess.PIPE)
        self.updater = P.stdout
        self.exclude = exclude
        self.wait_time = 600

    def get_devices_status(self):
        devices_table = cmd_output('nmcli device')
        return read_fwf(devices_table)

    def get_wifi_networks(self, ifname):
        cmd = f'nmcli dev wifi list --rescan auto ifname {ifname}'
        wifi_aps = cmd_output(cmd)
        return read_fwf(wifi_aps)

    def output(self):
        try:
            devs = self.get_devices_status()
        except IndexError:
            return '...'
        output = '%{A:NM_MENU:}'
        for dev_name, dev_type, dev_state, dev_con in zip(
                devs['DEVICE'], devs['TYPE'], devs['STATE'], devs['CONNECTION']):
            if dev_name == 'lo' or dev_name in self.exclude or dev_name.startswith('veth'):
                continue
            output += '%{A3:NMIFINFO_'+dev_name+':}'
            if dev_type == 'wifi' and dev_state == 'connected':
                wifi_nets = self.get_wifi_networks(dev_name)
                try:
                    wifi_signal = float(wifi_nets['SIGNAL'][wifi_nets['SSID'].index(dev_con)])
                except ValueError:
                    wifi_signal = 100
                signal_icn = list(' ▁▂▃▄▅▆▇█')
                wifi_icon = signal_icn[int(80*(len(signal_icn)-1)/100)]
                # wifi_icon = '󰤟' if wifi_signal < 25 else '󰤢' if wifi_signal < 50 else '󰤥' if wifi_signal < 75 else '󰤨'
                # bars = wifi_nets['BARS'][wifi_nets['SSID'].index(dev_con)]
                output += '%{A2:WIFIQR_'+dev_name+':}'
                output += wifi_icon
                output += '%{A2}'
                # output += bars
            elif dev_type == 'wifi' and dev_state == 'disconnected':
                output += ficon('\uf1eb', cdict['orange'])
            elif dev_type == 'wifi' and dev_state in ['disabled', 'unavailable']:
                output += ficon('\uf1eb', cdict['red'])
            elif dev_type == 'wifi' and dev_state == 'unmanaged':
                output += ficon('\uf1eb', cdict['dimmed'])
            elif dev_type == 'ethernet' and dev_state == 'connected':
                output += ficon('\uf796', cdict['green'])
            elif dev_type == 'ethernet' and dev_state == 'connecting':
                output += ficon('\uf796', cdict['light_yellow'])
            elif dev_type == 'ethernet' and dev_state in ['unavailable', 'disconnected']:
                output += ficon('\uf796', cdict['orange'])
            elif dev_type == 'ethernet' and dev_state == 'unmanaged':
                output += ficon('\uf796', cdict['dimmed'])
            output += '%{A3}'
        return output + '%{A}'

    def command(self, event):
        if event == 'NM_MENU':
            subprocess.Popen(
                'rofi -show nmcli -modi nmcli:~/Scripts/RofiMenus/nmcli-menu.py',
                shell=True, text=True)
        elif event.startswith('WIFIQR'):
            ifname = event.split("_")[-1]
            subprocess.Popen(f'konsole --hold -e nmcli dev wifi show ifname {ifname}', shell=True, text=True)
        elif event.startswith('NMIFINFO'):
            ifname = event.split("_")[-1]
            dev_info = cmd_output(f'nmcli dev show {ifname}')
            subprocess.Popen(f'dunstify -a "NetworkManager" "{ifname.upper()} INFO" "{dev_info}"',
                             shell=True, text=True)


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
        return ('%{A:PACMAN:}'+ficon('\uf466', cdict['l_yellow']) +
                f'{self.cache}%{{A}}')

    def command(self, event):
        if event.startswith('PACMAN'):
            subprocess.Popen('konsole -e pikaur -Su', text=True, shell=True)


class DiskUsage():
    def __init__(self, mount_point, icon=None):
        self.wait_time = 9000
        self.updater = None
        self.mount_point = mount_point
        self.icon = icon

    def output(self):
        df_out = cmd_output('df')
        if df_out:
            used_mnt = [line for line in df_out.split('\n')
                        if line.endswith(self.mount_point)]
            if used_mnt:
                icon = ficon(self.icon)
                return icon + used_mnt[0].split()[-2]
        return 'N/A'

    def command(self, event):
        pass


class SARCPUUsage():
    def __init__(self):
        self.wait_time = 30
        sar_thread = threading.Thread(target=self.sar_thread)
        sar_thread.start()
        self.updater = None
        self.cache = ""
        self.icon = '\uf2db'

    def output(self):
        cpu = self.cache
        if cpu.startswith('Linux') or len(cpu.split('\n')) > 1:
            return ficon(self.icon)+' '
        else:
            cpu_usage = sum(map(float, cpu.split()[3:6]))
            if cpu_usage >= 85:
                return (ficon(self.icon, cdict['red']) +
                        f'{cpu_usage:0.0f}%%')
            else:
                return ficon(self.icon)+f'{cpu_usage:0.0f}%%'

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
        self.wait_time = 30
        self.updater = None
        self.cache = []
        self.exclude = exclude

    def get_ip_out(self):
        '''parse the json output of ip command'''
        iface = cmd_output('ip -s -j link')
        ifaces = [
            (d['ifname'],
             d['stats64']['rx']['bytes']/1000,
             d['stats64']['tx']['bytes']/1000)
            for d in json.loads(iface)
            if not any(x in d['ifname'].lower() for x in self.exclude)
            and (d['operstate'] == 'UP' or (d['operstate'] == 'UNKNOWN'
                                           and 'UP' in d['flags']))]
        return ifaces

    def output(self):
        '''lemonbar ready output'''
        updt = self.wait_time
        ifaces = self.get_ip_out()
        iftxt_len = 3
        print(ifaces)
        if len(ifaces) == len(self.cache):
            speeds = [
                (ifaces[i][0] if len(ifaces[i][0]) < iftxt_len
                 else ifaces[i][0][:iftxt_len],
                 round((ifaces[i][1]-self.cache[i][1])/updt),
                 round((ifaces[i][2]-self.cache[i][2])/updt))
                for i in range(len(ifaces))]
        else:
            speeds = [
                (ifaces[i][0][:iftxt_len],
                 0, 0) for i in range(len(ifaces))]
        dwnicn = ficon('\uf103', cdict['green'], beforepad=5, afterpad=5)
        upicn = ficon('\uf102', cdict['orange'], beforepad=5, afterpad=2)
        formated_speeds = '/ '.join(
            (f'%{{F{cdict["teal"]}}}{x[0].upper()}%{{F-}} '
             f'{x[2]}'+upicn+f'{x[1]}'+dwnicn)
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
            return (ficon('\uf0ac', cdict['green']) +
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
        self.wait_time = 30
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
            return '%{F'+cdict['red']+'}'+ficon(icon)+str(round(avg_temp))+'%{F-}'
        else:
            return ficon(icon)+str(round(avg_temp))

    def command(self, event):
        pass


class GPUTemp():
    def __init__(self):
        self.wait_time = 30
        self.updater = None
        self.icons_dict = {50: '\uf2cb', 60: '\uf2ca', 70: '\uf2c9',
                           80: '\uf2c8', 90: '\uf2c7'}

    def output(self):
        gpu_temp = int(cmd_output('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader'))
        icon = [v for k, v in self.icons_dict.items() if k >= gpu_temp or k == 90][0]
        if gpu_temp > 80:
            return '%{F'+cdict['red']+'}'+ficon(icon)+str(round(gpu_temp))+'G%{F-}'
        else:
            return ficon(icon)+str(round(gpu_temp))+'G'

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
            return ('%{F'+cdict['red']+'}'+ficon(self.icon)+
                    f'{cpu_usage:0.1f}%{{F-}}')
        else:
            return (ficon(self.icon)+f'{cpu_usage:0.1f}%')

    def command(self, event):
        pass


class RamUsage():
    def __init__(self, percent=False):
        self.wait_time = 30
        self.updater = None
        self.icon = '\uf538'
        self.percent = percent

    def output(self):
        ram = cmd_output('vmstat -s').split('\n')
        used = int(ram[1].strip().split()[0])/(1024**2)
        total = int(ram[0].strip().split()[0])/(1024**2)
        percent = f'{used/total:0>3.0%}%'
        if self.percent and used/total > 0.85:
            return ('%{F'+cdict['red']+'}'+ficon(self.icon)+f'{percent}'+'%{F-}')
        elif self.percent:
            return ficon(self.icon, cdict['green'])+f'{percent}'
        elif not self.percent and used/total > 0.85:
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
            charging = 'Charging' in battery
            battery = battery.split(': ')[1].split(', ')[1]
            bat_vlu = int(battery.rstrip('%'))
            # literal % should be passed as %% to lemonbar
            battery += '%'
            icon = [v for k, v in self.icons.items() if k >= bat_vlu][0]
            if bat_vlu <= 5:
                return '%{F'+cdict['red']+'}'+ficon(icon)+battery+'%{F-}'
            elif bat_vlu == 100:
                return '%{F'+cdict["green"]+'}'+ficon(icon)+battery+'%{F-}'
            elif charging:
                return '%{F'+cdict["l_yellow"]+'}'+ficon(icon)+battery+'%{F-}'
            else:
                return ficon(icon)+battery

    def command(self, event):
        pass


class QtileWorkspaces():
    try:
        from libqtile.command_client import InteractiveCommandClient as ICC
        from libqtile.ipc import IPCError
        IMPORTED = True
    except ImportError:
        IMPORTED = False
    def __init__(self):
        if not IMPORTED:
            self.ouput = lambda: ""
            return
        P = subprocess.Popen(
            os.path.expanduser('~/.config/bspwm/bar/qtile_signal_handler.py'),
            text=True, stdout=subprocess.PIPE, encoding='UTF-8')
        self.updater = P.stdout
        self.wait_time = 60
        self.icc = self.ICC()

    def output(self):
        try:
            return self.__output()
        except self.IPCError:
            while True:
                try:
                    time.sleep(1)
                    del self.icc
                    self.icc = self.ICC()
                    return self.__output()
                except ConnectionRefusedError:
                    continue

    def __output(self):
        grps = self.icc.groups()
        all_workspaces = [grp for grp in grps.keys() if not grp == 'scratchpad']
        just_len = len(max(all_workspaces, key=len))
        empty_workspaces = [grp for grp in grps.keys()
                            if not grp == 'scratchpad' and len(grps[grp]['windows']) == 0]
        current = self.icc.group.info()['name']

        pre1 = '%{A:QTILE_WIDGETdesk'
        pre2 = '%{A4:QTILE_WIDGETnext:}'
        pre3 = '%{A5:QTILE_WIDGETprev:}'
        formatted_ws = []
        for w in all_workspaces:
            wor = f' {w} '
            # wor = '%{T3}'+w.center(just_len+2)+'%{T1}'
            # wor = w
            if w == current:
                formatted_ws.append('%{R}'+wor+'%{R}')
            # elif w in urgent:
            #     formatted_ws.append(
            #         pre1+w+':}'+'%{U'+cdict['red']+'}%{+o}'+wor+'%{-o}%{U-}%{A}')
            elif w in empty_workspaces:
                formatted_ws.append(
                    pre1+w+':}'+'%{U'+cdict['cyan']+'}%{+o}'+wor+'%{-o}%{U-}%{A}')
            else:
                formatted_ws.append(
                    pre1+w+':}'+wor+'%{A}')
        return pre2+pre3+''.join(formatted_ws)+'%{A5}%{A4}'

    def command(self, event):
        if event.startswith('QTILE_WIDGETdesk'):
            w = event.strip()[16:]
            self.icc.screen.toggle_group(w)
        elif event in ['QTILE_WIDGETnext', 'QTILE_WIDGETprev']:
            if event.endswith('next'):
                self.icc.screen.next_group()
            if event.endswith('prev'):
                self.icc.screen.prev_group()


class HerbstluftwmWorkspaces():
    def __init__(self, icons_dict=None, numbers=False):
        P = subprocess.Popen(
            "herbstclient --idle 'tag_changed|tag_flags'",
            text=True, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
        self.updater = P.stdout
        self.wait_time = 60
        self.icns = icons_dict
        self.numbers = numbers

    def output(self):
        tags_status = cmd_output('herbstclient tag_status')
        pre1 = '%{A:HERBST_WIDGETdesk'
        pre2 = '%{A4:HERBST_WIDGETnext:}'
        pre3 = '%{A5:HERBST_WIDGETprev:}'
        sfx = '%{-o}%{U-}%{A}'
        format_dict = {':': None, '-': 'orange', '.': 'cyan',
                       '!': 'red', '#': 'current'}
        formatted_ws = []
        for i, w in enumerate(tags_status.split('\t')):
            wor = f' {w[1:]} '
            if self.icns and not self.numbers:
                wor = ficon(self.icns.get(w[1:], ''), beforepad=5, afterpad=5)
            elif self.numbers:
                wor = f' {i} ' 
            clr = format_dict.get(w[0], None)
            if clr:
                if clr == 'current':
                    formatted_ws.append('%{R}'+wor+'%{R}')
                    continue
                formatted_ws.append(
                    pre1+w[1:]+':}'+(('%{U'+cdict[clr]+'}') if clr else '')+
                    '%{+o}'+wor+sfx)
            else:
                formatted_ws.append(pre1+w[1:]+':}'+wor+'%{A}')
                
        return pre2+pre3+''.join(formatted_ws)+'%{A5}%{A4}'

    def command(self, event):
        if event.startswith('HERBST_WIDGETdesk'):
            w = event.strip()[17:]
            print(w)
            subprocess.Popen(f'herbstclient use {w}', text=True, shell=True)
        elif event in ['HERBST_WIDGETnext', 'HERBST_WIDGETprev']:
            event = "-1" if event[-4:] == 'prev' else "+1"
            subprocess.Popen(f'herbstclient use_index {event}',
                             text=True, shell=True)


class HerbstluftwmWorkspacesDots():
    def __init__(self):
        P = subprocess.Popen("herbstclient --idle 'focus_changed|tag_changed'", text=True, shell=True,
                             stdout=subprocess.PIPE, encoding='UTF-8')
        self.updater = P.stdout
        self.wait_time = 60

    def output(self):
        wor_count = int(cmd_output('herbstclient attr tags.count'))
        all_workspaces = [cmd_output(f'herbstclient attr tags.{i}.name')
                          for i in range(wor_count)]
        just_len = len(max(all_workspaces, key=len))
        empty_workspaces, urgent_tags = [], []
        for desk in all_workspaces:
            wins_count = cmd_output(f"herbstclient attr tags.by-name.{desk}.client_count")
            urgent_count = cmd_output(f'herbstclient attr tags.by-name.{desk}.urgent_count')
            urgent_count = 0 if urgent_count == '' else urgent_count
            if int(wins_count) == 0:
                empty_workspaces.append(desk)
            if int(urgent_count) != 0:
                urgent_tags.append(desk)
        current = cmd_output('herbstclient attr tags.focus.name').strip()

        pre1 = '%{A:HERBST_WIDGETdesk'
        pre2 = '%{A4:HERBST_WIDGETnext:}'
        pre3 = '%{A5:HERBST_WIDGETprev:}'
        formatted_ws = []
        for w in all_workspaces:
            wor = ''
            suffix = '%{T-}%{-o}%{U-}%{A}'
            spacing = str(3*GDKSCALE)
            other_side = str(int(spacing)-9*GDKSCALE)
            if w == current:
                if w in empty_workspaces:
                    wor = ''
                formatted_ws.append(
                    '%{R}%{O'+spacing+'}%{T2}'+wor+'%{T-}%{R}'+'%{O'+
                    other_side+'}')
            elif w in urgent_tags:
                formatted_ws.append(
                    pre1+w+':}'+'%{U'+cdict['red']+'}%{+o}%{O'+
                    spacing+'}%{T2}'+wor+suffix+'%{O'+other_side+'}')
                # 7 is the fixed spacing afterward this symbol that needs to be removed
            elif w in empty_workspaces:
                wor = ''
                formatted_ws.append(
                    pre1+w+':}'+'%{O'+spacing+'}%{T2}'+wor+'%{T-}%{A}'+'%{O'+
                    other_side+'}')
            else:
                formatted_ws.append(
                    pre1+w+':}%{O'+spacing+'}%{T2}'+wor+'%{T-}%{A}'+
                    '%{O'+other_side+'}')

        return pre2+pre3+''.join(formatted_ws)+'%{A5}%{A4}'

    def command(self, event):
        if event.startswith('HERBST_WIDGETdesk'):
            w = event.strip()[17:]
            print(w)
            subprocess.Popen(f'herbstclient use {w}', text=True, shell=True)
        elif event in ['HERBST_WIDGETnext', 'HERBST_WIDGETprev']:
            event = "-1" if event[-4:] == 'prev' else "+1"
            subprocess.Popen(f'herbstclient use_index {event}',
                             text=True, shell=True)


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
            wor = f' {w} '
            # wor = '%{T3}'+w.center(just_len+2)+'%{T1}'
            # wor = w
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
        self.wait_time = 30
        self.updater = None
        self.icons = {0: '\uf026', 25: '\uf027', 100: '\uf028'}
        self.actions = {
            'max': 'pactl set-sink-volume @DEFAULT_SINK@ 100%',
            'mute': 'pactl set-sink-volume @DEFAULT_SINK@ 0',
            'increase': 'pactl set-sink-volume @DEFAULT_SINK@ +2%',
            'decrease': 'pactl set-sink-volume @DEFAULT_SINK@ -2%'
        }

    def output(self):
        vol = cmd_output('pamixer --get-volume')
        vol = vol if vol != '' else '0'
        prefix = ('%{A3:pactlmax:}%{A:pactlmute:}%{A4:pactlincrease:}'
                  '%{A5:pactldecrease:}')

        icon = [v for k, v in self.icons.items()
                if k >= int(vol) or k == 100][0]
        suffix = '%{A5}%{A4}%{A}%{A3}'
        return prefix+ficon(icon)+f'{int(vol):02d}%%'+suffix

    def command(self, event):
        
        if event.startswith('pactl'):
            action = self.actions[event.lstrip('pactl')]
            subprocess.Popen(action, text=True, shell=True)
        return True


class UdiskieMenu():
    def __init__(self):
        self.wait_time = 0
        self.updater = None
        self.icon = '\uf0a0'

    def output(self):
        return '%{A:udiskie_menu:}'+ficon(self.icon, beforepad=2, afterpad=2)+'%{A}'

    def command(self, event):
        if event == 'udiskie_menu':
            subprocess.Popen(
                'rofi -show udiskie -modi udiskie:~/Scripts/RofiMenus/udiskie-menu.py',
                shell=True, text=True)


class SyncthingIndicator():
    def __init__(self):
        self.wait_time = 600
        self.updater = None
        self.icon = '\uf021'
        self.text = '0/0'

    def output(self):
        syncthing_json = cmd_output('syncthing cli show connections')
        color = cdict['dimmed']
        if syncthing_json:
            sync_conn = json.load(StringIO(syncthing_json))
            connected = len([v for v in sync_conn['connections'].values()
                            if v['connected']])
            self.text = f'{connected}/{len(sync_conn["connections"])}'
            color = cdict['dimmed'] if connected == 0 else cdict['green']
        
        return '%{A:syncthing:}'+ficon(self.icon, color)+self.text+'%{A}'

    def get_guiaddress(self):
        try:
            address = json.load(StringIO(cmd_output(
                'syncthing cli show system')))['guiAddressUsed']
        except json.decoder.JSONDecodeError:
            address = 'localhost'
        return address
        
    def command(self, event):
        if event == 'syncthing':
            address = self.get_guiaddress()
            subprocess.Popen(
                f'xdg-open http://{address}',
                shell=True, text=True)


class XAutoLocker():
    def __init__(self):
        self.wait_time = 6000
        self.updater = None
        self.coffee_on = '\uf7b6'
        self.coffee = '\uf0f4'
        self.lock = '\uf023'
        self.enabled = False

    def output(self):
        coffee = ficon(self.coffee_on if self.enabled else self.coffee, cdict['green'] if self.enabled else cdict['dimmed'])
        lock = ficon(self.lock, cdict['l_yellow'])
        return '%{A:XAUTOLOCK:}'+coffee+'%{A}%{A:XAUTOLOCKNOW:}'+lock+'%{A}'

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
        

class PodsBuddy():
    def __init__(self, pods_mac='C0:D1:93:F0:78:0E'):
        self.wait_time = 30
        self.updater = None
        self.bt_icon = '\uf294'
        self.icon = '\uf025'
        self.pods_mac = pods_mac

    def output(self):
        self.powered = 'Powered: yes' in cmd_output('bluetoothctl show')
        bt_icon = ficon(self.bt_icon, idx=3, color=cdict['green']
                             if self.powered else cdict['dimmed'])
        self.connected = 'Connected: yes' in cmd_output('bluetoothctl info')
        icon = ficon(self.icon, cdict['green']
                          if self.connected else cdict['dimmed'])
        return '%{A:BLUETOOTH:}'+bt_icon+'%{A}%{A:POD:}%{A3:HARDPOD:}'+icon+'%{A3}%{A}'

    def command(self, event):
        if event == 'BLUETOOTH':
            P = subprocess.Popen(f'bluetoothctl power {"off" if self.powered else "on"}'.split())
            P.wait()
            return True
        elif event == 'POD':
            P = subprocess.Popen(f'bluetoothctl {"disconnect" if self.connected else "connect"} {self.pods_mac}'.split())
            P.wait()
            return True
        elif event == 'HARDPOD':
            P = subprocess.Popen(';'.join([
                'rfkill block bluetooth',
                'bluetoothctl power off',
                'sleep 1',
                'rfkill unblock bluetooth',
                'bluetoothctl power on',
                'sleep 2',
                f'bluetoothctl remove {self.pods_mac}',
                f'bluetoothctl pair {self.pods_mac}',
                'sleep 2',
                f'bluetoothctl trust {self.pods_mac}',
                f'bluetoothctl connect {self.pods_mac}'
            ]), shell=True)
            return True


class DarkLightSwitcher():
    def __init__(self):
        self.wait_time = 120
        self.updater = None
        self.light_icon = '\uf185'
        self.dark_icon = '\uf186'
        self.mode_path = os.path.expanduser('~/.config/THEME_VARIANT')

    def output(self):
        if os.path.exists(self.mode_path):
            with open(self.mode_path) as f:
                current_mode = f.read()
        else:
            current_mode = 'dark'
        out = (ficon(self.light_icon, swap=current_mode != 'dark')+
               ficon(self.dark_icon, swap=current_mode == 'dark'))
        return '%{A:DARKMODE_SWITCH:}'+out+'%{A}'

    def command(self, event):
        if event == 'DARKMODE_SWITCH':
            P = subprocess.Popen(os.path.expanduser('~/Scripts/switch_dark_light.py'))
            P.wait()
            return True


class SafeEyes():
    def __init__(self):
        self.wait_time = 600
        self.updater = None
        self.icon = '\uf06e'
        self.text = '∞ mins'

    def output(self):
        status = cmd_output('safeeyes --status')
        if 'not running' in status:
            color = cdict['dimmed']
            icon = ficon(self.icon, color)
            return '%{A:safeeyesEnable:}'+f'{icon}{self.text}'+'%{A}'
        else:
            color = None
            next_break = status.split('at ')[1].strip()

        return '%{A:syncthing:}'+ficon(self.icon, color)+self.text+'%{A}'

    def command(self, event):
        if event == 'syncthing':
            subprocess.Popen(
                'xdg-open localhost:8080',
                shell=True, text=True)


class TimeDate():
    def __init__(self, timeformat=None):
        self.wait_time = 60
        self.updater = None
        self.timeformat = timeformat
        self.month_year = (datetime.date.today().year,
                            datetime.date.today().month)
        self.txt_cal = calendar.TextCalendar()

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
        date_time = ('%{A:currentcal:}%{A4:nextcal:}%{A5:prevcal:}' +
                     ficon('\uf073', cdict['orange'])+'%{A5}%{A4}%{A}' +
                     datetime.datetime.strftime(now, '%a %d-%b,%y %H:%M'))
        return date_time+ficon(' \uf017')

    def command(self, event):
        if event == 'currentcal':
            self.month_year = (datetime.date.today().year,
                               datetime.date.today().month)
        elif event == 'nextcal':
            if self.month_year[1] == 12:
                self.month_year = (self.month_year[0]+1, 1)
            else:
                self.month_year = (self.month_year[0], self.month_year[1]+1)
        elif event == 'prevcal':
            if self.month_year[1] == 1:
                self.month_year = (self.month_year[0]-1, 12)
            else:
                self.month_year = (self.month_year[0], self.month_year[1]-1)
        if event in ['currentcal', 'nextcal', 'prevcal']:
            cal = self.txt_cal.formatmonth(*self.month_year)
            cal_hdr = cal.splitlines()[0]
            cal_body = '\n'.join(cal.splitlines()[1:])
            subprocess.Popen(
                (f'dunstify -i office-calendar "{cal_hdr}" "{cal_body}" '
                 '-r 000010 -h "string:desktop-entry:calendar_popup"'),
                shell=True, text=True)


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

