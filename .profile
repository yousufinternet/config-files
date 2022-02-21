export MOZ_ENABLE_WAYLAND=1
export XDG_CONFIG_HOME="$HOME/.config"
export QT_QPA_PLATFORMTHEME=qt5ct
export EDITOR='emacsclient -c -a ""'
export RTV_EDITOR='emacsclient -c -a ""'

# my scripts and flutter executables
export PATH=$PATH:$HOME/.local/bin
export PATH=$HOME/.local/bin/flutter/bin:$PATH
export PATH=$HOME/.local/bin/flutter/bin/cache/dart-sdk/bin:$PATH
export PATH=$HOME/.pub-cache/bin/:$PATH
export NODE_PATH=$NODE_PATH:$(npm root -g)

# for java applications
export AWT_TOOLKIT=MToolkit
