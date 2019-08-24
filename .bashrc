#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export EDITOR=vim
export RTV_EDITOR=vim
alias ar5='aria2c -c -V -s 5 --max-connection-per-server=5'
alias ls='ls --color=auto'
alias resrvserv='ssh yusuf@10.127.188.192'
alias mediacenter='ssh yusuf@192.168.1.109'
alias worklaptop='ssh archie-work@192.168.1.107'
PS1='[\u@\h \W]\$ '

# vi mode in bash
set -o vi

if [ -z "$GDK_SCALE" ]; then
	export GDK_SCALE=1
fi

export ROFI_DPI=$((GDK_SCALE*100))
alias android='xrandr --output eDP-1 --mode 1920x1080; genymotion-player --vm-name "Custom Phone - 8.0 - API 26 - 768x1280"; xrandr --output eDP-1 --mode 3840x2160'

# infinite history and erase duplicates
export HISTTIMEFORMAT="%d/%m/%y %T "
HISTSIZE=
HISTFILESIZE=
HISTCONTROL=erasedups

# Had to use that with mlterm
export TERM=xterm-256color

# Supposedly text should wrap as the terminal size changes
shopt -s checkwinsize

# change to a dir by typing its name or path
shopt -s autocd

# Powerline prompt
powerline-daemon -q
POWERLINE_BASH_CONTINUATION=1
POWERLINE_BASH_SELECT=1
. /usr/lib/python3.7/site-packages/powerline/bindings/bash/powerline.sh

eval "$(fasd --init auto)"

if xset q &>/dev/null; then
  screenfetch | lolcat
  cowsay -f tux $(fortune) | lolcat -t
fi
