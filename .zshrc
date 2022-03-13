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
export EDITOR='emacsclient -c -a ""'
export PAGER='more'
export TERMINAL="konsole"
export RTV_EDITOR='emacsclient -c -a ""'
export PATH=$PATH:$HOME/.local/bin
export PATH=$HOME/.config/bspwm/scripts/:$PATH
export NODE_PATH=$NODE_PATH:$(npm root -g)

# Aliases
alias radiogolha='cvlc mms://www.radiogolha.net/RadioGolha'
alias ar5="aria2c -c -V -s 5 --max-connection-per-server=5 --on-download-complete=ding.sh"
alias ls='ls --color=auto --hyperlink=always'

alias resrvserv='mosh yusuf@10.127.188.92'
alias mediacenter='mosh yusuf@yusufs-macbookpro'
alias worklaptop='mosh yusuf@yusufs-dell'
alias lenovolaptop='mosh yusuf@yusufs-lenovo'

alias ec='emacsclient -a "" -c'

alias gst='git status'
alias gd='git diff'
alias gad='git add'

alias pacman='sudo pacman --color=always'
alias hcat="highlight -O ansi --force"
alias eclrun='WINEPREFIX=~/.wine32 WINEARCH=win32 wine ~/.wine32/drive_c/ecl/macros/eclrun.exe'
alias adb_input="adb shell input keyevent"
alias youtube_pip='mpv --slang=en --force-window=immediate --no-terminal --geometry=25%x25%-0-0 --autofit=1280x720 --ytdl-format="bestvideo[height<=?720][fps<=?30]+bestaudio/best" --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched=,cookies="~/Downloads/cookies.txt",embed-subs=,sub-lang=en,write-sub=,write-auto-sub='

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

#startx
if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi

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
