# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=2000
SAVEHIST=1000

# avoid duplicates in history
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS

# Grabbed from manjaro zsh config
# https://github.com/Chrysostomus/manjaro-zsh-config/blob/master/manjaro-zsh-config
setopt correct                                                  # Auto correct mistakes
setopt extendedglob                                             # Extended globbing. Allows using regular expressions with *
setopt nocaseglob                                               # Case insensitive globbing
setopt numericglobsort                                          # Sort filenames numerically when it makes sense
setopt appendhistory                                            # Immediately append history instead of overwriting
setopt histignorealldups                                        # If a new command is a duplicate, remove the older one
setopt inc_append_history                                       # save commands are added to the history immediately, otherwise only when shell exits.
setopt histignorespace                                          # Don't save commands that start with space

zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'       # Case insensitive tab completion
zstyle ':completion:*' rehash true                              # automatically find new executables in path 
zstyle ':completion:*' use-cache on

setopt autocd notify
bindkey -v
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/yusuf/.zshrc'

autoload -Uz compinit
autoload -Uz promptinit
# End of lines added by compinstall
compinit

# arrow style completion
zstyle ':completion:*' menu select
zstyle ':completion::complete:*' gain-privileges 1

promptinit
prompt clint

# Environment
export PAGER='less'  # used to use more for colors, but the bindings are messed up in more
export TERMINAL="konsole"
export RTV_EDITOR='emacsclient -c -a ""'
export PATH=$PATH:$HOME/.local/bin
export PATH=$HOME/.config/bspwm/scripts/:$PATH
export NODE_PATH=$NODE_PATH:$(npm root -g)

# Colors for less
export LESS_TERMCAP_mb=$'\e[1;32m'
export LESS_TERMCAP_md=$'\e[1;32m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[01;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;4;31m'

# from https://dt.iki.fi/unclutter-home-dir to declutter the home directory
# XDG directories
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_DATA_HOME="$HOME/.local/share"

export GNUPGHOME="$XDG_DATA_HOME/gnupg"

# jetbrains.com/help/go/configuring-goroot-and-gopath.html
export GOPATH="$XDG_CACHE_HOME/go"

# doc.rust-lang.org/cargo/reference/environment-variables.html
export CARGO_HOME="$XDG_CACHE_HOME/cargo"

export NPM_CONFIG_USERCONFIG='$XDG_CONFIG_HOME/npm/rc'

export JDK_JAVA_OPTIONS="-Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel -Dsun.java2d.opengl=true -Duser.home=$XDG_DATA_HOME/java"

export WINEPREFIX="$XDG_DATA_HOME/wine"

# Aliases
alias radiogolha='cvlc mms://www.radiogolha.net/RadioGolha'
alias ar5="aria2c -c -V -s 5 --max-connection-per-server=5 --on-download-complete=ding.sh"
alias ls='ls --color=auto --hyperlink=always'

alias resrvserv='mosh yusuf@10.127.188.92'
alias mediacenter='mosh yusuf@yusufs-macbookpro'
alias worklaptop='mosh yusuf@yusufs-dell'
alias lenovolaptop='mosh yusuf@yusufs-lenovo'

alias ec='emacsclient -a "" -c'
alias lf='~/.config/lf/lfub'
alias sysr='sudo systemctl restart'
alias syse='sudo systemctl enable --now'
alias sysd='sudo systemctl disable --now'
alias sysc='sudo systemctl'

alias gst='git status'
alias gd='git diff'
alias gad='git add'

alias pacman='sudo pacman --color=always'
alias hcat="highlight -O ansi --force"
alias eclrun='WINEPREFIX=~/.wine32 WINEARCH=win32 wine ~/.wine32/drive_c/ecl/macros/eclrun.exe'
alias adb_input="adb shell input keyevent"
alias youtube_pip='prime-run mpv --slang=en --force-window=immediate --no-terminal --geometry=25%x25%-0-0 --autofit=1280x720 --ytdl-format="bestvideo[height<=?720][fps<=?30]+bestaudio/best" --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched=,cookies="~/Downloads/cookies.txt",embed-subs=,sub-lang=en,write-sub=,write-auto-sub='
alias net_phone='adb connect `ssh root@192.168.1.1 ip r | head -n 1 | cut -f 3 -d " "`;scrcpy -m 720 --max-fps 10 --no-audio -s `ssh root@192.168.1.1 ip r | head -n 1 | cut -f 3 -d " "`'

# always set GDK_SCALE, if not set in global environment variables set it to 1
if [ -z "$GDK_SCALE" ]; then
	export GDK_SCALE=1
fi

# include git info in prompt
# Autoload zsh add-zsh-hook and vcs_info functions (-U autoload w/o substition, -z use zsh style)
autoload -Uz add-zsh-hook vcs_info
# Enable substitution in the prompt.
setopt prompt_subst
# Run vcs_info just before a prompt is displayed (precmd)
add-zsh-hook precmd vcs_info

zstyle ':vcs_info:*' check-for-changes true
zstyle ':vcs_info:*' unstagedstr '*'
zstyle ':vcs_info:*' stagedstr '+'
zstyle ':vcs_info:git:*' formats       '%b%u%c'


# Custom prompt
export PS1='${${KEYMAP/vicmd/-N-}/(main|viins)/-I-}%F{magenta}[%f %F{green}%n%f:%F{yellow}%B%1~%f%b %F{magenta}]%f %F{cyan}[%f %B${vcs_info_msg_0_}%b %F{cyan}]%f %B%#%b%F{green}>%f'
export PS2="%F{green}>%f "
export RPS1="<%w %T %F{blue}[%h]%f"

#ipython style history search
autoload -Uz up-line-or-beginning-search down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search

[[ -n "${key[Up]}"   ]] && bindkey -- "${key[Up]}"   up-line-or-beginning-search
[[ -n "${key[Down]}" ]] && bindkey -- "${key[Down]}" down-line-or-beginning-search

# startx
 if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
   exec startx
fi


# if [ "$(tty)" = "/dev/tty1" ]; then
	# exec sway --my-next-gpu-wont-be-nvidia
#	exec qtile start --backend wayland
# fi

# zoxide
eval "$(zoxide init zsh)"

# search for new executables everytime
zstyle ':completion:*' rehash true

# automatically suggest what to install
function command_not_found_handler {
    local purple='\e[1;35m' bright='\e[0;1m' green='\e[1;32m' reset='\e[0m'
    printf 'zsh: command not found: %s\n' "$1"
    local entries=(
        ${(f)"$(/usr/bin/pacman -F --machinereadable -- "/usr/bin/$1")"}
    )
    if (( ${#entries[@]} ))
    then
        printf "${bright}$1${reset} may be found in the following packages:\n"
        local pkg
        for entry in "${entries[@]}"
        do
            # (repo package version file)
            local fields=(
                ${(0)entry}
            )
            if [[ "$pkg" != "${fields[2]}" ]]
            then
                printf "${purple}%s/${bright}%s ${green}%s${reset}\n" "${fields[1]}" "${fields[2]}" "${fields[3]}"
            fi
            printf '    /%s\n' "${fields[4]}"
            pkg="${fields[2]}"
        done
    fi
}

# Syntax highlight and autosuggestions
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# https://feldspaten.org/2018/11/20/zsh-and-home-end-delete-buttons/
# ctrl-left and ctrl-right
bindkey "\e[1;5D" backward-word
bindkey "\e[1;5C" forward-word
# ctrl-bs and ctrl-del
bindkey "\e[3;5~" kill-word
bindkey "\C-_"    backward-kill-word
# del, home and end
bindkey "\e[3~" delete-char
bindkey "\e[H"  beginning-of-line
bindkey "\e[F"  end-of-line
# alt-bs
bindkey "\e\d"  undo
# Reverse search
bindkey '^R' history-incremental-search-backward

fortune | cowsay -f tux | lolcat -p 3

