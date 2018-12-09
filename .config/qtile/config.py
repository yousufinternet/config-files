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
from libqtile.config import Key, ScratchPad, DropDown, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os, subprocess
from powerline.bindings.qtile.widget import PowerlineTextBox

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

mod = "mod4"
terminal = "konsole"
scale_factor = int(os.environ.get('GDK_SCALE', 1))

# Startup apps
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


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
    Key([mod], "c", lazy.group["scratchpad"].dropdown_toggle("calc")),

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

    # Swap panes of split stack
    Key([mod, "control"], "Return", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Apps shortcuts
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "e", lazy.spawn("rofi -show run -dpi %s -theme Monokai -modi run,drun,window,windowcd,ssh" % str(100*scale_factor))),
    Key([mod, "control"], "w", lazy.spawn("optirun qutebrowser")),
    Key([mod, "control"], "n", lazy.spawn("konsole --profile NewsBoat --notransparency -e newsboat -r")),
    Key([mod, "shift"], "f", lazy.spawn("krusader")),
    Key([mod, "control"], "f", lazy.spawn("%s -e ranger" % terminal)),
    Key([mod, "control"], "e", lazy.spawn("emacs")),
    Key([mod, "shift"], "e", lazy.spawn("oblogout")),
    Key([mod, "control"], "h", lazy.spawn("%s -e htop" % terminal)),
    Key([mod, "control"], "m", lazy.spawn("%s -e ncmpcpp" % terminal)),
    Key([mod, "control"], "x", lazy.spawn("xkill")),

    # Brightness and Volume controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 2")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 5")),
    Key([mod], "b", lazy.spawn("/home/yusuf/.config/i3/toggle_brightness.py")),
    # Key([mod, "control"], "z", lazy.spawn("killall vmg; sudo optirun vmg")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [
    ScratchPad("scratchpad",
               [DropDown("term", 'konsole', opacity=0.8),
                DropDown("calc", "kcalc", on_focus_lost_hide=False, opacity=0.8, y=0.5, x=0.5, width=0.28)])] + [
                    Group(str(x+1)+':'+i) for x, i in enumerate("")] + [
                        Group('0:', spawn=["%s -e ncmpcpp" % terminal, "%s -e htop" % terminal])]

for x, i in enumerate(groups):
    x = 0 if x == 10 else x
    if not i.name == "scratchpad":
        keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], str(x), lazy.group[i.name].toscreen()),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], str(x), lazy.window.togroup(i.name)),
        ])

layouts = [
    layout.Max(),
    # layout.Columns(fair=True, margin=20),
    layout.Wmii(margin=20),
    layout.Stack(num_stacks=2),
    layout.Matrix(),
    layout.xmonad.MonadTall()
]

widget_defaults = dict(
    font='Noto color emoji',
    fontsize=13 * scale_factor,
    padding=3,
)
extension_defaults = widget_defaults.copy()

alt_font = 'Noto Sans Display'
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(disable_drag=True, highlight_color='2473ff',
                                highlight_method="line", background='ffffff',
                                foreground='000000', active='000000',
                                inactive='b9b9b9'),
                widget.Image(filename='~/.config/qtile/power7.png'),
                widget.Prompt(),
                widget.CurrentLayoutIcon(),
                widget.TaskList(highlight_method="block", rounded=False,
                                font=alt_font, fontsize=13*scale_factor,
                                iconsize=18*scale_factor, border='0056ea'),
                widget.Image(filename='~/.config/qtile/power3.png'),
                widget.Mpd2(fontsize=24, background="0056ea"),
                widget.Image(filename='~/.config/qtile/power6.png', background='009700'),
                # widget.Spacer(length=500),
                widget.TextBox('📦', background='009700'),
                widget.CheckUpdates(execute='konsole -e "pacaur -Syu --noconfirm"', display_format=':{updates}', font=alt_font, background='009700'),
                widget.Image(filename='~/.config/qtile/power5.png'),
                widget.NetGraph(graph_color="fff500"),
                widget.CPUGraph(),
                widget.ThermalSensor(font=alt_font),
                widget.MemoryGraph(graph_color="00ff00"),
                widget.Backlight(backlight_name="intel_backlight", update_interval=1, font=alt_font),
                widget.KeyboardLayout(update_interval=0.2),
                widget.BatteryIcon(),
                widget.Image(filename='~/.config/qtile/power2.png'),
                widget.TextBox('📅', background="ff5e00"),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', background="ff5e00", font=alt_font),
                widget.TextBox('🕐', background="ff5e00"),
                widget.Image(filename='~/.config/qtile/power1.png'),
                widget.Systray(icon_size=16*scale_factor, padding=7*scale_factor),
            ],
            36,
            opacity=0.8
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
bring_front_click = False
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
])
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
