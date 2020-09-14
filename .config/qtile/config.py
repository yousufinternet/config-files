# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import signal
import libqtile
import logging
from libqtile.config import Key, ScratchPad, DropDown, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile.command_client import InteractiveCommandClient
from libqtile import layout, bar, widget, hook
import os, subprocess
# from powerline.bindings.qtile.widget import PowerlineTextBox

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

try:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    from gi.repository.GLib import Variant as gi_variant
    FAILED_NOTIFY = False
except Exception:
    FAILED_NOTIFY = True
mod = "mod4"
terminal = os.path.expanduser("~/.config/bspwm/scripts/mlterm_rand_bg.py")

# Detect if the screen is HiDPI or not
scale_factor = int(os.environ.get('GDK_SCALE', 1))

# If optirun is installed then hybrid graphics exist on system, if not don't
# prepend optirun to some commands
cmd = "pacman -Qe | grep 'bumblebee'"
hybrid_grphcs = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True,
                                 shell=True).communicate()[0] != ''


Notify.init("notifications")
notification = Notify.Notification.new("", "")
# Startup apps
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


def kill_all_windows():
    @lazy.function
    def __inner(qtile):
        for window in qtile.currentGroup.windows:
            window.kill()
    return __inner


def kill_all_windows_except_current():
    @lazy.function
    def __inner(qtile):
        for window in qtile.currentGroup.windows:
            if window != qtile.currentWindow:
                window.kill()
    return __inner


def current_win_alwaysontop():
    @lazy.function
    def __inner(qtile):
        subprocess.Popen(
            [os.path.expanduser('~/.config/qtile/always_ontop.py'), '--store'])
    return __inner


@hook.subscribe.client_killed
@hook.subscribe.client_focus
@hook.subscribe.client_urgent_hint_changed
@hook.subscribe.changegroup
@hook.subscribe.client_new
def update_bar(*args):
    pid_path = '/tmp/qtile_signal_handler_pid'
    if os.path.exists(pid_path):
        with open(pid_path, 'r') as f_obj:
            pid = f_obj.read().strip()
        os.kill(int(pid), signal.SIGUSR1)


# @hook.subscribe.client_new
# def floating_wins_always_above(window):
#     logging.error(str(dir(window.window)))
#     cur_group = window.group.info()['name']
#     wins = window.windows()
#     floating_wins = [win['id'] for win in wins if win['floating'] and win['group'] == cur_group]
#     for win in floating_wins:
#         qtile.window[win].bring_to_front()

@hook.subscribe.client_new
def floating_wins_always_above(*args):
    subprocess.Popen(os.path.expanduser('~/.config/qtile/floating_wins_always_above.py'))

def no_win_alwaysontop():
    @lazy.function
    def __inner(qtile):
        os.remove(os.path.expanduser('~/.config/qtile/alwaysontop_win'))
    return __inner


def volume_ctl_old(vol):
    '''
    Will be kept as an example on how to use notify-send
    '''
    @lazy.function
    def __inner(qtile):
        sign = '+' if vol > 0 else '-'
        subprocess.Popen(
            f"pactl set-sink-volume @DEFAULT_SINK@ {sign}{abs(vol)}%",
            shell=True, text=True)
        cur_vol = int(subprocess.Popen(
            'pamixer --get-volume', shell=True, text=True,
            stdout=subprocess.PIPE).communicate()[0][:-1])
        icon = 'audio-volume-muted'
        if cur_vol >= 70:
            icon = 'audio-volume-high'
        elif cur_vol >= 40:
            icon = 'audio-volume-medium'
        elif cur_vol > 0:
            icon = 'audio-volume-low'
        subprocess.Popen(f'notify-send -i {icon} -t 1500 -h int:value:{cur_vol} -h string:synchronous:volume "Volume changed"', shell=True, text=True)
    return __inner


def brightness_ctl(vlu):
    @lazy.function
    def __inner(qtile):
        symbol = 'A' if vlu > 0 else 'U'
        subprocess.Popen(
            f"light -{symbol} {abs(vlu)}",
            shell=True, text=True)
        if not FAILED_NOTIFY:
            cur_bright = float(subprocess.Popen(
                'light', shell=True, text=True,
                stdout=subprocess.PIPE).communicate()[0][:-1])
            icon = 'display-brightness-off'
            if cur_bright >= 70:
                icon = 'display-brightness-high'
            elif cur_bright >= 40:
                icon = 'display-brightness-medium'
            elif cur_bright > 0:
                icon = 'display-brightness-low'
            notification.update('Brightness Changed', '', icon)
            notification.set_hint('value', gi_variant.new_int32(cur_bright))
            notification.show()
    return __inner


def volume_ctl(vol):
    @lazy.function
    def __inner(qtile):
        sign = '+' if vol > 0 else '-'
        subprocess.Popen(
            f"pactl set-sink-volume @DEFAULT_SINK@ {sign}{abs(vol)}%",
            shell=True, text=True)
        if not FAILED_NOTIFY:
            cur_vol = int(subprocess.Popen(
                'pamixer --get-volume', shell=True, text=True,
                stdout=subprocess.PIPE).communicate()[0][:-1])
            icon = 'audio-volume-muted'
            if cur_vol >= 70:
                icon = 'audio-volume-high'
            elif cur_vol >= 40:
                icon = 'audio-volume-medium'
            elif cur_vol > 0:
                icon = 'audio-volume-low'
            notification.update('Volume Changed', '', icon)
            notification.set_hint('value', gi_variant.new_int32(cur_vol))
            notification.show()
    return __inner


def moveto_next_empty_group():
    @lazy.function
    def __inner(qtile):
        subprocess.Popen(
            os.path.expanduser('~/.config/qtile/tonext_emptygroup.py'))
    return __inner


def to_next_empty_group():
    @lazy.function
    def __inner(qtile):
        subprocess.Popen(
            os.path.expanduser('~/.config/qtile/next_emptygroup.py'))
    return __inner


def to_urgent(qtile):
    cg = qtile.currentGroup
    for group in qtile.groupMap.values():
        if group == cg:
            continue
        if len([w for w in group.windows if w.urgent]) > 0:
            qtile.currentScreen.setGroup(group)
            return


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    # Key([mod, "control"], "Left", lazy.screen.prev_group()),
    # Key([mod, "control"], "Right", lazy.screen.next_group()),
    Key([mod, "control"], "Left", lazy.layout.prev()),
    Key([mod, "control"], "Right", lazy.layout.next()),
    Key([mod], "v", to_next_empty_group()),
    Key([mod, 'shift'], "v", moveto_next_empty_group()),
    Key([mod], "a", current_win_alwaysontop()),
    Key([mod, 'shift'], "a", no_win_alwaysontop()),

    # DropDown Terminal
    Key([mod], "d", lazy.group["scratchpad"].dropdown_toggle("term")),

    # easy to reach calculator
    Key([mod], "c", lazy.group["scratchpad"].dropdown_toggle("calc")),
    Key([mod, 'shift'], "i", lazy.group["scratchpad"].dropdown_toggle("ipython")),

    # toggle floating
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    # toggle fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Resize windows
    Key([mod], "x", lazy.layout.grow_right()),
    Key([mod], "z", lazy.layout.grow_left()),
    Key([mod, "shift"], "x", lazy.layout.grow()),
    Key([mod, "shift"], "z", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "m", lazy.group["scratchpad"].dropdown_toggle("pulsemixer")),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # useful when floating windows get buried
    Key([mod], "grave", lazy.window.bring_to_front()),

    # Swap panes of split stack
    Key([mod, "control"], "Return", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    Key([mod, "control"], "x", lazy.spawn("xkill")),
    # probably the -B option will need i3lock-color package

    # Key([mod, "control"], "z", lazy.spawn("killall vmg; sudo optirun vmg")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, 'shift'], "q", kill_all_windows()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "F12", lazy.function(to_urgent)),
]

layouts = [
    layout.Max(),
    layout.Columns(
        fair=True, margin=4*scale_factor, border_width=4*scale_factor,
        border_normal='d79921', border_focus='d65d0e'),
    layout.Stack(num_stacks=2),
    layout.Matrix(),
    layout.xmonad.MonadTall()
]

groups = [
    ScratchPad(
        "scratchpad",
        [DropDown("term", f"{terminal} -e tmux -2", opacity=0.9, height=0.5),
         DropDown("calc", "kcalc", on_focus_lost_hide=False,
                  opacity=0.8, y=0.5, x=0.5, width=0.28),
         DropDown(
             "ipython", f"{terminal} -e ipython", on_focus_lost_hide=False,
             opacity=0.9, y=0, x=0.6, width=0.4, height=1)])] + [
        Group(str(x)) for x in range(1, 11)]

for x, i in enumerate(groups):
    x = 0 if x == 10 else x
    if not i.name == "scratchpad":
        keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], str(x), lazy.group[i.name].toscreen()),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], str(x), lazy.window.togroup(i.name)),
        ])

# screens = [Screen()]
screens = [Screen()]

# screens = [
#     Screen(
#         bottom=bar.Bar(
#             [
#                 widget.GroupBox(disable_drag=True, highlight_color='d65d0e',
#                                 highlight_method="line", background='504945',
#                                 foreground='928374', active='fbf1c7',
#                                 inactive='665c54', font=alt_font,
#                                 this_current_screen_border='fb4934',
#                                 other_current_screen_border='fb4934',
#                                 fontsize=15*scale_factor, urgent_alert_method='line'),
#                 widget.TextBox('', foreground='504945', background='3c3836',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power7.png'),
#                 widget.Prompt(),
#                 widget.CurrentLayoutIcon(),
#                 widget.TaskList(highlight_method="block", rounded=False,
#                                 font=alt_font, fontsize=13*scale_factor,
#                                 iconsize=18*scale_factor, border='d65d0e'),
#                 widget.TextBox('', foreground='#3c3836', background='98971a',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power3.png'),
#                 widget.TextBox('', foreground='98971a', background='689d6a',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power6.png', background='009700'),
#                 # widget.Spacer(length=500),
#                 widget.TextBox('📦', background='689d6a'),
#                 widget.CheckUpdates(execute='konsole -e "pacaur -Syu --noconfirm"', display_format=':{updates}', font=alt_font, background='689d6a'),
#                 widget.TextBox('', foreground='689d6a', background='3c3836',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power5.png'),
#                 widget.NetGraph(graph_color="fabd2f", width=50*scale_factor),
#                 widget.CPUGraph(width=50*scale_factor, graph_color='fb4934'),
#                 widget.MemoryGraph(graph_color="b8bb26", width=50*scale_factor),
#                 widget.TextBox('', foreground='3c3836', background='d79921',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power8.png'),
#                 widget.ThermalSensor(font=alt_font, background='d79921'),
#                 widget.TextBox('', background='3c3836', foreground='d79921',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power9.png'),
#                 widget.KeyboardLayout(update_interval=0.2,
#                                       configured_keyboards=['us', 'ara'],
#                                       padding=2*scale_factor,
#                                       fontshadow='000000'),
#                 widget.BatteryIcon(),
#                 # widget.Image(filename='~/.config/qtile/power2.png'),
#                 widget.TextBox('', foreground='3c3836', background='928374',
#                                fontsize=20*scale_factor, padding=0),
#                 widget.TextBox('📅', background="928374"),
#                 widget.Clock(format='%a %d-%B %I:%M %p', background="928374", font=alt_font),
#                 widget.TextBox('🕐', background="928374"),
#                 widget.TextBox('', foreground='928374', background='3c3836',
#                                fontsize=20*scale_factor, padding=0),
#                 # widget.Image(filename='~/.config/qtile/power1.png'),
#                 widget.Backlight(backlight_name="intel_backlight", update_interval=1, font=alt_font),
#                 widget.Systray(icon_size=16*scale_factor, padding=7*scale_factor),
#             ],
#             20 * scale_factor, background='#3c3836'
#         ),
#     ),
# ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False # Default is False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'xfce4-appfinder'},
    {'wmclass': 'kcalc'},
    {'wmclass': 'gcr-prompter'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wmclass': 'pinentry-gtk-2'},
    {'wmclass': 'Pinentry-gtk-2'},
    {'wmclass': 'xfce4-panel'},
    {'wname': 'xfce4-panel'},
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
], border_focus="d65d0e", border_normal="fabd2f")
auto_fullscreen = True
focus_on_window_activation = "smart"

# @libqtile.hook.subscribe.client_focus
# def raise_mpv_ontop(c):
#     try:
#         error='None'
#         client_obj = Client()
#         # cur_win = client_obj.window.name
#         win_lst = client_obj.group.info()['windows']
#         mpv_win = list(win for win in win_lst if 'mpv' in win) 
#         if len(mpv_win) == 0:
#             return
#         mpv_win = mpv_win[0]
#         while True:
#             match = client_obj.window.match(wname=mpv_win)
#             if match:
#                 break
#             else:
#                 client_obj.group.next_window()
#         client_obj.group.window.enable_floating()
#         client_obj.group.window.bring_to_front()
#         c.focus()
#     except Exception as e:
#         error = e
#     with open('/home/yusuf/debug_floating.txt', 'w+') as f_obj:
#         f_obj.write(error)
#         f_obj.write('test')

@libqtile.hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()


# @libqtile.hook.subscribe.focus_change
# def float_mpv():
#     subprocess.Popen(os.path.expanduser('~/.config/qtile/always_ontop.py'))

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
