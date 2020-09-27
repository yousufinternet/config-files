
# Help
opens a rofi menu with all man pages, displays the selected man page in zathura


***super*** ***+*** ***shift*** ***+*** ***F1***
```bash
   ~/.config/bspwm/scripts/browse_man_pages.py
```
\vspace{12pt}
open bspwm man page as pdf in zathura


***super*** ***+*** ***F1***
```bash
   man -Tpdf bspc | zathura -
```
\vspace{12pt}
open sxhkdrc help


***super*** ***+*** ***ctrl*** ***+*** ***F1***
```bash
   $HOME/.config/bspwm/scripts/sxhkdrc_help.py
```
\vspace{12pt}
# Terminal
open the terminal


***super*** ***+*** ***Return***
```bash
   $TERMINAL -e tmux -2
```
\vspace{12pt}
# Rofi
all open windows


***super*** ***+*** ***w***
```bash
   rofi -show window -terminal $TERMINAL -dpi 0 -theme $ROFI_THEME -modi\
   window,windowcd
```
\vspace{12pt}
start an application


***super*** ***+*** ***e***
```bash
   rofi -show-icons -terminal $TERMINAL -show run -dpi 0 -theme $ROFI_THEME \
   -modi run,drun,ssh
```
\vspace{12pt}
# Screenshots
fullscreen screenshot


***@Print***
```bash
   spectacle --background
```
\vspace{12pt}
Select region for screenshot


***@shift+Print***
```bash
   spectacle --background --region
```
\vspace{12pt}
# Brightness/Volume
Raise/Lower Brightness/Volume


***XF86Audio\{Raise,Lower\}Volume***
```bash
   volume_ctl.sh {+5,-10}
```
\vspace{12pt}
Increase/decrease brightness


***\{\_,shift+\}XF86MonBrightness\{Up,Down\}***
```bash
   brightness_ctl.sh {+5,+1,-5,-1}
```
\vspace{12pt}
Toggle screen brightness between 1%/100%


***super*** ***+*** ***shift*** ***+*** ***b***
```bash
   toggle_brightness.py
```
\vspace{12pt}
Raise/Lower volume


***super+\{shift+,\_\}\{equal,minus\}***
```bash
   {brightness_ctl.sh,volume_ctl.sh} {+5,-5}
```
\vspace{12pt}
# BSPWM
## Layouts
alternate between the tiled and monocle layout


***super*** ***+*** ***Tab***
```bash
   bspc desktop -l next
```
\vspace{12pt}
put current window in its own tabbed window, remove it from tabbed, or tab all windows


***super*** ***+*** ***t;*** ***\{c,r,a\}***
```bash
   tabbed_company.py {create,remove,all}
```
\vspace{12pt}
join current window with tabbed in DIR


***super*** ***+*** ***t;*** ***\{Left,Up,Down,Right\}***
```bash
   tabbed_company.py join $(bspc query -N -n {west,north,south,east})
```
\vspace{12pt}
Mark the current desktop as tiled


***super*** ***+*** ***shift*** ***+*** ***t***
```bash
   set_tiled.py
```
\vspace{12pt}
## Moving windows
swap the current node and the biggest node


***super*** ***+*** ***s***
```bash
   bspc node -s biggest.local
```
\vspace{12pt}
move a single floating window into the corner


***super*** ***+*** ***v***
```bash
   ~/.config/bspwm/scripts/move_floating.py
```
\vspace{12pt}
Rotate nodes


***super+\{\_,shift\}+r***
```bash
   bspc node {@/ --rotate 90,@parent --rotate 270}
```
\vspace{12pt}
Preselect a direction to spawn new windows into or move existing window


***super+ctrl+\{Left,Right,Up,Down\}***
```bash
   bspc node --presel-dir {\~west,\~east,\~north,\~south}
```
\vspace{12pt}
Move the focused window into a preselection


***super+a***
```bash
   bspc node --to-node `bspc query -N -n '.!automatic'`
```
\vspace{12pt}
## Resizing
resize root node to 30%/70%


***super*** ***+\{\_,*** ***shift*** ***+\}*** ***z***
```bash
   bspc node @/ --ratio {0.3,0.7}
```
\vspace{12pt}
Inrease decrease windows gaps in current desktop


***super*** ***+*** ***\{F7,F8\}***
```bash
   bspc config -d focused window_gap $((`bspc config -d focused window_gap` {+,-} $((8*GDK_SCALE)) ))
```
\vspace{12pt}
Set windows gaps in current desktop to 0


***super*** ***+*** ***F9***
```bash
   bspc config -d focused window_gap 0
```
\vspace{12pt}
balance nodes


***super*** ***+*** ***b***
```bash
   bspc node @/ --balance
```
\vspace{12pt}
contract a window by moving one of its side inward


***super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***\{h,j,k,l\}***
```bash
   resize.py {left,down,up,right} $((GDK_SCALE*30))
```
\vspace{12pt}
contract a window by moving one of its side inward


***super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***\{Left,Down,Up,Right\}***
```bash
   ~/.config/bspwm/scripts/resize.py {left,down,up,right} $((GDK_SCALE*30))
```
\vspace{12pt}
## Window states
close/kill focused node


***super*** ***+*** ***\{\_,shift*** ***+*** ***\}*** ***q***
```bash
   tab_aware_close.py {close,kill}
```
\vspace{12pt}
toggle window state tiled/floating/fullscreen


***super*** ***+*** ***\{space,f\}***
```bash
   bspc node -t {\~floating,\~fullscreen}
```
\vspace{12pt}
make current window sticky


***super*** ***+*** ***\{shift*** ***+*** ***s,m,x\}***
```bash
   bspc node --flag {sticky,\~marked,hidden}
```
\vspace{12pt}
restore/replace current node with hidden


***super*** ***+*** ***\{ctrl,shift\}*** ***+*** ***x***
```bash
   ~/.config/bspwm/scripts/replace_with_hidden.py {show,swap}
```
\vspace{12pt}
hide all windows except focused


***super*** ***+*** ***alt*** ***+*** ***x***
```bash
   ~/.config/bspwm/scripts/hide_all.py
```
\vspace{12pt}
Select a window to kill


***@super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***k***
```bash
   xkill
```
\vspace{12pt}
## Desktops and monitors
focus desktop {1-9,0} (or bounce to last desktop)


***super*** ***+*** ***\{1-9,0\}***
```bash
   target='focused:^{1-9,10}'; \
   [ "$(bspc query -D -d "$target")" != "$(bspc query -D -d)" ] \
   && bspc desktop -f "$target" || bspc desktop -f last.local
```
\vspace{12pt}
send to the given desktop


***super*** ***+*** ***shift*** ***+*** ***\{1-9,0\}***
```bash
   bspc node --to-desktop 'focused:^{1-9,10}'
```
\vspace{12pt}
move and switch windows between monitors


***super*** ***+*** ***\{\_,shift*** ***+\}*** ***\{comma,*** ***period\}***
```bash
   bspc {monitor --focus,node --to-monitor} {prev,next}
```
\vspace{12pt}
## Session Control
Lock screen


***super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***x***
```bash
   i3lock -e -B --force-clock --keylayout 0 --insidecolor 1e58a46a --indicator
```
\vspace{12pt}
shutdown menu


***super*** ***+*** ***shift*** ***+*** ***e***
```bash
   oblogout
```
\vspace{12pt}
Quit bspwm


***super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***q***
```bash
   bspc quit
```
\vspace{12pt}
Restart bspwm


***@super*** ***+*** ***ctrl*** ***+*** ***shift*** ***+*** ***r***
```bash
   xfce4-panel -r -d;\
   bspc wm --restart
```
\vspace{12pt}
## Selecting windows
focus the node in the given direction


***super*** ***+*** ***\{\_,shift*** ***+*** ***\}\{h,j,k,l\}***
```bash
   bspc node --{focus,to-node} {west,south,north,east}
```
\vspace{12pt}
focus the node in the given direction


***super*** ***+*** ***\{\_,shift*** ***+*** ***\}\{Left,Down,Up,Right\}***
```bash
   bspc node --{focus,to-node} {west,south,north,east}
```
\vspace{12pt}
switch between windows when in monocle mode


***super*** ***+*** ***\{\_,shift*** ***+*** ***\}*** ***c***
```bash
   bspc node --focus '{next,prev}.local.!hidden.window'
```
\vspace{12pt}
focus the node for the given path jump


***super*** ***+*** ***\{p,o\}***
```bash
   bspc node -f @{parent,brother}
```
\vspace{12pt}
# Apps
# terminal apps
Terminal apps with large font size


***super*** ***+*** ***i*** ***;*** ***\{m,h,n,r,f,p,s\}***
```bash
   $TERMINAL -w $((23*GDK_SCALE)) -e {ncmpcpp,htop,newsboat,tuir --enable-media,lf,podboat -C ~/.config/podboat/config,pulsemixer}
```
\vspace{12pt}
File manager


***super*** ***+*** ***ctrl*** ***+*** ***f***
```bash
   $TERMINAL -e ranger
```
\vspace{12pt}
# GUI apps
GUI apps with no need for graphics card acceleration


***super*** ***+*** ***g*** ***;*** ***\{c,f,g,t,q,r,z\}***
```bash
   {calibre, foliate, gimp, telegram-desktop, transmission-qt, remmina, zeal}
```
\vspace{12pt}
GUI apps that require graphics card assistance (via optirun)


***super*** ***+*** ***shift*** ***+*** ***g*** ***;*** ***\{f,d\}***
```bash
   start_with_optirun.sh {firefox,darktable}
```
\vspace{12pt}
Web browser


***super*** ***+*** ***ctrl*** ***+*** ***w***
```bash
   start_with_optirun.sh qutebrowser
```
\vspace{12pt}
IDE


***super*** ***+*** ***ctrl*** ***+*** ***e***
```bash
   emacsclient -c -a ""
```
\vspace{12pt}
# Scratchpad
Terminal dropdown


***super*** ***+*** ***d***
```bash
   $HOME/.config/bspwm/scripts/scratchpad_term.py -c dropdown_term -w 0.8 \
   -ht 0.65 -x 0.1 -y $((GDK_SCALE*20)) --termflags -e tmux -2
```
\vspace{12pt}
calculator dropdown


***super*** ***+*** ***ctrl*** ***+*** ***c***
```bash
   $HOME/.config/bspwm/scripts/scratchpad_term.py -c dropdown_calc -w 0.3 \
   -ht 0.3 -x 0.35 -y 0.7 --termflags -e bc
```
\vspace{12pt}
ipython dropdown


***super*** ***+*** ***ctrl*** ***+*** ***i***
```bash
   $HOME/.config/bspwm/scripts/scratchpad_term.py -c dropdown_ipython -w 0.3 \
   -ht 0.8 -x 0.7 -y 0.1 --termflags -e ipython
```
\vspace{12pt}
# Reload sxhkd
make sxhkd reload its configuration files:


***super*** ***+*** ***Escape***
```bash
   pkill -USR1 -x sxhkd
```
\vspace{12pt}