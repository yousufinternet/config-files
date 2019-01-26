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

import libqtile
from libqtile.config import Key, ScratchPad, DropDown, Screen, Group, Drag, Click, Match
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
import os, subprocess
# from powerline.bindings.qtile.widget import PowerlineTextBox

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

mod = "mod4"
terminal = "qterminal"

# Detect if the screen is HiDPI or not
scale_factor = int(os.environ.get('GDK_SCALE', 1))

# If optirun is installed then hybrid graphics exist on system, if not don't
# prepend optirun to some commands
cmd = "pacman -Ql | grep 'optirun'"
hybrid_grphcs = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True,
                                 shell=True).communicate()[0] != ''

# Startup apps
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


def floating_mpv(qtile):
    current_group = qtile.currentGroup
    win_names = [w.name for w in current_group.windows]
    win_dict = {w.name: w for w in current_group.windows}
    path = os.path.expanduser('~/windows')
    with open(path, 'w+') as f:
        f.write(' '.join(win_names))
    for w in current_group.windows:
        wn = w.name
        with open(path + wn[:5], 'w+') as f:
            f.write(wn)
        if 'mpv' in wn.lower():
            try:
                w.cmd_bring_to_front()
                # libqtile.manager.window.Window.cmd_bring_to_front(w, qtile)
            except Exception as e:
                with open(path + '(mpv)', 'w+') as f:
                    f.write(str(dir(w)) + str(e))




def toggle_bar(qtile):
    libqtile.manager.Qtile.cmd_hide_show_bar(qtile)


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
    Key([mod, "control"], "Left", lazy.screen.prev_group()),
    Key([mod, "control"], "Right", lazy.screen.next_group()),

    # DropDown Terminal
    Key([mod], "d", lazy.group["scratchpad"].dropdown_toggle("term")),

    # easy to reach calculator
    Key([mod], "c", lazy.group["scratchpad"].dropdown_toggle("calc")),
    Key([mod, 'shift'], "h", lazy.group["scratchpad"].dropdown_toggle("htop")),
    Key([mod, 'shift'], "m", lazy.group["scratchpad"].dropdown_toggle("ncmpcpp")),

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
    Key([mod], "m", lazy.layout.maximize()),

    # Screenshots
    Key([], "Print", lazy.spawn("gnome-screenshot")),
    Key(["shift"], "Print", lazy.spawn("gnome-screenshot -a")),

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

    # Apps shortcuts
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "e", lazy.spawn("rofi -show-icons -show run -dpi %s -theme ~/.cache/wal/colors-rofi-dark.rasi -modi run,drun,window,windowcd,ssh" % str(100*scale_factor))),
    Key([mod], "w", lazy.spawn("rofi -show windowcd -dpi %s -theme Monokai -modi windowcd,window" % str(100*scale_factor))),
    Key([mod, "control"], "w", lazy.spawn("optirun qutebrowser" if hybrid_grphcs else "qutebrowser")),
    Key([mod, "control"], "n", lazy.spawn("konsole --profile NewsBoat --notransparency -e newsboat -r")),
    Key([mod, "shift"], "f", lazy.spawn("krusader")),
    Key([mod, "control"], "f", lazy.spawn("%s -e ranger" % terminal)),
    Key([mod, "control"], "e", lazy.spawn("emacs")),
    Key([mod, "shift"], "e", lazy.spawn("oblogout")),
    Key([mod, "control"], "h", lazy.spawn("%s -e htop" % terminal)),
    # Key([mod, "control"], "m", lazy.spawn("%s -e ncmpcpp" % terminal)),
    Key([mod, "control"], "x", lazy.spawn("xkill")),
    Key([mod, "control"], "m", lazy.function(floating_mpv)),
    # probably the -B option will need i3lock-color package
    Key([mod, "shift", "control"], "x",
        lazy.spawn("i3lock -B=%s" % 4*scale_factor)),

    # Brightness and Volume controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 2")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 5")),
    Key([mod], "b", lazy.spawn(os.path.expanduser("~/.config/i3/toggle_brightness.py"))),
    # Key([mod, "control"], "z", lazy.spawn("killall vmg; sudo optirun vmg")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "F12", lazy.function(to_urgent)),
    Key([mod, 'shift'], 'b', lazy.function(toggle_bar)),
]

layouts = [
    layout.Max(),
    layout.Columns(fair=True, margin=8*scale_factor,
                   border_normal='d79921', border_focus='d65d0e'),
    # layout.Wmii(margin=8*scale_factor, border_normal='d79921', border_focus='d65d0e', border_normal_stack='fb4934', border_focus_stack='cc241d'),
    layout.Stack(num_stacks=2),
    layout.Matrix(),
    layout.xmonad.MonadTall()
]

groups = [
    ScratchPad("scratchpad",
               [DropDown("term", terminal, opacity=0.8),
                DropDown("calc", "kcalc", on_focus_lost_hide=False, opacity=0.8, y=0.5, x=0.5, width=0.28),
                DropDown("htop", "konsole -e htop", on_focus_lost_hide=False,
                         opacity=0.9, y=0, x=0, width=0.4, height=1),
                DropDown("ncmpcpp", "konsole -e ncmpcpp", on_focus_lost_hide=False,
                         opacity=0.9, y=1-0.4, x=0.25, width=0.5, height=0.4)])] + [
                    Group(str(x+1)) for x in range(8)] + [
                       Group('9', matches=[Match(wm_class=['Steam', 'steam'])]),
                       Group('10', layout='matrix', spawn=[
                           "%s -e ncmpcpp" % terminal, "%s -e htop" % terminal,
                           "%s -e tmux -2" % terminal, terminal])]

for x, i in enumerate(groups):
    x = 0 if x == 10 else x
    if not i.name == "scratchpad":
        keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], str(x), lazy.group[i.name].toscreen()),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], str(x), lazy.window.togroup(i.name)),
        ])

widget_defaults = dict(
    # font='Noto color emoji',
    font='RobotoMono Nerd Font',
    fontsize=13*scale_factor,
    padding=3 if scale_factor == 2 else 1,
)
extension_defaults = widget_defaults.copy()

alt_font = 'RobotoMono Nerd Font'
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(disable_drag=True, highlight_color='d65d0e',
                                highlight_method="line", background='504945',
                                foreground='928374', active='fbf1c7',
                                inactive='665c54', font=alt_font,
                                this_current_screen_border='fb4934',
                                other_current_screen_border='fb4934',
                                fontsize=15*scale_factor, urgent_alert_method='line'),
                widget.TextBox('', foreground='504945', background='3c3836',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power7.png'),
                widget.Prompt(),
                widget.CurrentLayoutIcon(),
                widget.TaskList(highlight_method="block", rounded=False,
                                font=alt_font, fontsize=13*scale_factor,
                                iconsize=18*scale_factor, border='d65d0e'),
                widget.TextBox('', foreground='#3c3836', background='98971a',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power3.png'),
                widget.Mpd2(fontsize=12*scale_factor, background="98971a"),
                widget.TextBox('', foreground='98971a', background='689d6a',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power6.png', background='009700'),
                # widget.Spacer(length=500),
                widget.TextBox('📦', background='689d6a'),
                widget.CheckUpdates(execute='konsole -e "pacaur -Syu --noconfirm"', display_format=':{updates}', font=alt_font, background='689d6a'),
                widget.TextBox('', foreground='689d6a', background='3c3836',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power5.png'),
                widget.NetGraph(graph_color="fabd2f", width=50*scale_factor),
                widget.CPUGraph(width=50*scale_factor, graph_color='fb4934'),
                widget.MemoryGraph(graph_color="b8bb26", width=50*scale_factor),
                widget.TextBox('', foreground='3c3836', background='d79921',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power8.png'),
                widget.ThermalSensor(font=alt_font, background='d79921'),
                widget.TextBox('', background='3c3836', foreground='d79921',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power9.png'),
                widget.KeyboardLayout(update_interval=0.2, padding=2*scale_factor, fontshadow='000000'),
                widget.BatteryIcon(),
                # widget.Image(filename='~/.config/qtile/power2.png'),
                widget.TextBox('', foreground='3c3836', background='928374',
                               fontsize=20*scale_factor, padding=0),
                widget.TextBox('📅', background="928374"),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', background="928374", font=alt_font),
                widget.TextBox('🕐', background="928374"),
                widget.TextBox('', foreground='928374', background='3c3836',
                               fontsize=20*scale_factor, padding=0),
                # widget.Image(filename='~/.config/qtile/power1.png'),
                widget.Backlight(backlight_name="intel_backlight", update_interval=1, font=alt_font),
                widget.Systray(icon_size=16*scale_factor, padding=7*scale_factor),
            ],
            20 * scale_factor, background='#3c3836'
        ),
    ),
]

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
bring_front_click = True # Default is False
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
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
], border_focus="d65d0e", border_normal="fabd2f")
auto_fullscreen = True
focus_on_window_activation = "smart"

@libqtile.hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
