#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# for java applications
export AWT_TOOLKIT=MToolkit

# git status in prompt
red='\e[0;31m'
RED='\e[1;31m'
green='\e[0;32m'
GREEN='\e[1;32m'
yellow='\e[0;33m'
YELLOW='\e[1;33m'
blue='\e[0;34m'
BLUE='\e[1;34m'
magenta='\e[0;35m'
MAGENTA='\e[1;35m'
cyan='\e[0;36m'
CYAN='\e[1;36m'
NC='\e[0m' # No Color

# Taken from http://www.opinionatedprogrammer.com/2011/01/colorful-bash-prompt-reflecting-git-status/
function _git_prompt() {
  local git_status="`git status -unormal 2>&1`"
  if ! [[ "$git_status" =~ Not\ a\ git\ repo ]]; then
    if [[ "$git_status" =~ nothing\ to\ commit ]]; then
      local ansi=$GREEN
    elif [[ "$git_status" =~ nothing\ added\ to\ commit\ but\ untracked\ files\ present ]]; then
      local ansi=$RED
    else
      local ansi=$YELLOW
    fi
    if [[ "$git_status" =~ On\ branch\ ([^[:space:]]+) ]]; then
      branch=${BASH_REMATCH[1]}
      #test "$branch" != master || branch=' '
    else
      # Detached HEAD.  (branch=HEAD is a faster alternative.)
      branch="(`git describe --all --contains --abbrev=4 HEAD 2> /dev/null ||
      echo HEAD`)"
    fi
    echo -n '[ \['"$ansi"'\]'"$branch"'\[\e[0m\] ]'
  fi
}

function report_status() {
  RET_CODE=$?
  if [[ $RET_CODE -ne 0 ]] ; then
    echo -ne "[\[$RED\]$RET_CODE\[$NC\]]"
  fi
}

# export _PS1="\[$NC\][\u@\h \W]"
# export PS2="\[$NC\]> "
# powerline
# PS1='[\u@\h \W]\$ '
export _PS1="\e[0;35m[\e[0m \e[2;36m\u\e[0m:\e[1;32m\W\e[0m \e[0;35m]\e[0m "
PS2=">>"
export PROMPT_COMMAND='_status=$(report_status);export PS1="${_PS1} $(_git_prompt)${_status} \e[1;31m\$\e[0m :-\n  ";unset _status;'

# Use bash-completion, if available
[[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && \
    . /usr/share/bash-completion/bash_completion

# cod completion
source <(cod init $$ bash)

# git completions
. /usr/share/git/completion/git-completion.bash

# for bspwm
export XDG_CONFIG_HOME="$HOME/.config"
# export ROFI_THEME=~/.config/rofi/themes/dracula.rasi
export ROFI_THEME=sidebar
export EDITOR=vim
# export TERMINAL="mlterm --fontsize=$((GDK_SCALE*15))"
export TERMINAL="konsole"
export RTV_EDITOR='emacsclient -c -a ""'

# my scripts and flutter executables
export PATH=$PATH:$HOME/.local/bin
export PATH=$HOME/.local/bin/flutter/bin:$PATH
export PATH=$HOME/.local/bin/flutter/bin/cache/dart-sdk/bin:$PATH
export PATH=$HOME/.pub-cache/bin/:$PATH
export PATH=$HOME/.config/bspwm/scripts/:$PATH
export NODE_PATH=$NODE_PATH:$(npm root -g)

alias radiogolha='cvlc mms://www.radiogolha.net/RadioGolha'
alias ar5="aria2c -c -V -s 5 --max-connection-per-server=5 --on-download-complete=ding.sh"
alias ls='ls --color=auto'
alias resrvserv='mosh yusuf@10.127.188.92'
alias mediacenter='mosh yusuf@192.168.1.110'
alias worklaptop='mosh archie-work@192.168.1.6'
alias android-emulator='~/Android/Sdk/emulator/emulator @Pixel_3_API_28'
alias ec='emacsclient -a "" -c'
alias all_cams_low='mpv $(cat Documents/Security-Cams/cam4.strm) & mpv $(cat Documents/Security-Cams/cam1.strm) & mpv $(cat Documents/Security-Cams/cam2.strm)'
alias all_cams_high='mpv $(cat Documents/Security-Cams_high/cam4.strm) & mpv $(cat Documents/Security-Cams_high/cam1.strm) & mpv $(cat Documents/Security-Cams_high/cam2.strm)'
alias gst='git status'
alias gd='git diff'
alias two_min_pen='for i in {0..120}; do printf "%03d\r" $i; sleep 1; done;mplayer /usr/share/games/xboard/sounds/penalty.wav'
alias pacman='sudo pacman --color=always'
alias hcat="highlight -O ansi --force"
alias gamescrcpy="prime-run scrcpy --max-fps 20 -w -S --disable-screensaver"
alias eclrun='WINEPREFIX=~/.wine32 WINEARCH=win32 wine ~/.wine32/drive_c/ecl/macros/eclrun.exe'
alias adb_input="adb shell input keyevent"

# vi mode in bash
set -o vi

if [ -z "$GDK_SCALE" ]; then
	export GDK_SCALE=1
fi

alias android='xrandr --output eDP-1 --mode 1920x1080; genymotion-player --vm-name "Custom Phone - 8.0 - API 26 - 768x1280"; xrandr --output eDP-1 --mode 3840x2160'

# infinite history and erase duplicates
export HISTTIMEFORMAT="%d/%m/%y %T "
HISTSIZE=
HISTFILESIZE=
HISTCONTROL=erasedups

# Supposedly text should wrap as the terminal size changes
shopt -s checkwinsize

# change to a dir by typing its name or path
shopt -s autocd

# Powerline prompt
# powerline-daemon -q
# POWERLINE_BASH_CONTINUATION=1
# POWERLINE_BASH_SELECT=1
# . /usr/lib/python3.9/site-packages/powerline/bindings/bash/powerline.sh

if xset q &>/dev/null; then
  # screenfetch | lolcat
  cowsay -f tux $(fortune) | lolcat -p 1
fi

# if [ "$(tty)" = "/dev/tty1" ]; then
# 	exec sway --my-next-gpu-wont-be-nvidia
# fi

if systemctl -q is-active graphical.target && [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi

# source ~/.local/share/blesh/ble.sh
