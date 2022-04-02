#!/usr/bin/env python
import os
import sys
import shlex
import subprocess as sp

configs_path = os.path.expanduser('~/.config')

def modify_conf(path, themes_dict, identify_line):
    with open(path, 'r') as f:
        conf_file = f.read()

    conf_file = '\n'.join([identify_line+themes_dict[switch_theme]
                           if ln.startswith(identify_line) else ln
                           for ln in conf_file.splitlines()])

    with open(path, 'w') as f:
        f.write(conf_file)

        
def readandswitch(switch_to='auto'):
    var_path = os.path.join(configs_path, 'THEME_VARIANT')
    if os.path.exists(var_path) and switch_to == 'auto':
        with open(var_path, 'r') as f:
            current_theme = f.read()
    else:
        current_theme = 'dark'
    switch_theme = 'light' if current_theme == 'dark' else 'dark'
    switch_theme = switch_theme if switch_to == 'auto' else switch_to
    with open(os.path.join(configs_path, 'THEME_VARIANT'), 'w+') as f:
        f.write(switch_theme)
    return current_theme, switch_theme


switch_to = 'auto'
if len(sys.argv) > 1:
    if sys.argv[1] not in ['dark', 'light']:
        raise ValueError('Please select dark or light only')
    switch_to = sys.argv[1]
current_theme, switch_theme = readandswitch(switch_to)

# define styles
qt5ct_style = {'dark': 'kvantum-dark', 'light': 'kvantum'}
kvantum_themes = {'dark': 'MateriaDark#', 'light': 'Materia'}
gtk2_themes = {'dark': '"Materia-dark"', 'light': '"Materia-light"'}
gtk_themes = {'dark': 'Materia-dark', 'light': 'Materia-light'}
icon_gtk2_themes = {'dark': '"Papirus-Dark"', 'light': '"Papirus-Light"'}
icon_themes = {'dark': 'Papirus-Dark', 'light': 'Papirus-Light'}
emacs_themes = {'dark': 'modus-vivendi', 'light': 'modus-operandi'}
konsole_profiles = {'dark': 'Default-Black.profile', 'light': 'Default-Light.profile'}
wallpapers = {'dark': '/usr/share/backgrounds/archlinux/geolanes.png',
              'light': '/usr/share/backgrounds/archlinux/wireparts.png'}

# modify qt5ct
modify_conf(os.path.join(configs_path, 'qt5ct/qt5ct.conf'),
            qt5ct_style, 'style=')
modify_conf(os.path.join(configs_path, 'Kvantum/kvantum.kvconfig'),
            kvantum_themes, "theme=")
modify_conf(os.path.join(configs_path, 'qt5ct/qt5ct.conf'),
            icon_themes, 'icon_theme=')

# modify konsolerc
modify_conf(os.path.join(configs_path, 'konsolerc'),
            konsole_profiles, 'DefaultProfile=')

# modify gtk2
modify_conf(os.path.expanduser('~/.gtkrc-2.0'), gtk2_themes, 'gtk-theme-name=')
modify_conf(os.path.expanduser('~/.gtkrc-2.0'), icon_gtk2_themes,
            'gtk-icon-theme-name=')

# modify gtk3
modify_conf(os.path.join(configs_path, 'gtk-3.0/settings.ini', ), gtk_themes, 'gtk-theme-name=')
modify_conf(os.path.join(configs_path, 'gtk-3.0/settings.ini', ),
            icon_themes, 'gtk-icon-theme-name=')

# change theme in emacs
sp.Popen(f'emacsclient -e "(my-load-theme \'{emacs_themes[switch_theme]})"', shell=True)

# update wallpaper
sp.Popen(['feh', '--bg-fill', shlex.quote(wallpapers[switch_theme])])
