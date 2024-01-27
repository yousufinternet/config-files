export MOZ_ENABLE_WAYLAND=1
export XDG_CONFIG_HOME="$HOME/.config"
export QT_QPA_PLATFORMTHEME=qt5ct
export EDITOR='emacsclient -c -a ""'
export RTV_EDITOR='emacsclient -c -a ""'
export TERMINAL="konsole"

# my scripts and flutter executables
export PATH=$PATH:$HOME/.local/bin
export PATH=$HOME/.local/bin/flutter/bin:$PATH
export PATH=$HOME/.local/bin/flutter/bin/cache/dart-sdk/bin:$PATH
export PATH=$HOME/.pub-cache/bin/:$PATH
export NODE_PATH=$NODE_PATH:$(npm root -g)

# for java applications
export AWT_TOOLKIT=MToolkit

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
