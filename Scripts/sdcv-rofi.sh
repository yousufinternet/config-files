#!/bin/sh

# Name    : sdcv-rofi
# About   : This is a rofi script to translate words and phrases with sdcv.
# Version : 2024-05-29
# License : MIT;
# Author  : Schimon Zackary Jehudah;

version="0.1"

if [ "$1" = "--help" ] ; then
  echo "Translate words or phrases and copy the results to clipboard."
  echo "dmenu and sdcv must be installed."
  echo "Either xclip, xsel or wl-paste is required."
  exit 0
elif [ "$1" = "--version" ] ; then
  echo "sdcv-dmenu version $version"
  exit 0
fi

case $XDG_SESSION_TYPE in
#  x11)
  /dev/pts/1)
    if [ -x "$(command -v xsel)" ]; then
      clipboard=$(xsel)
    elif [ -x "$(command -v xclip)" ]; then
      clipboard=$(xclip -out)
    else
      echo "xclip is required to use clipboard."
    fi
    ;;
  wayland)
    if [ -x "$(command -v wl-paste)" ]; then
      clipboard=$(wl-paste --primary)
    else
      echo "wl-paste is required to use clipboard."
    fi
    ;;
  *)
    echo "Could not determine display server."
    echo "Defaulting to xclip."
    if [ -x "$(command -v xclip)" ]; then
      clipboard=$(xclip -out)
    else
      echo "wl-paste is required to use clipboard."
    fi
    ;;
esac

chosen_option=$(echo -e "$clipboard\nClose" | rofi -dmenu -i -p "Translate" -mesg "Enter a word or phrase to translate.");

if [ -z "$chosen_option" ] || [ "$chosen_option" == "Close" ]; then
  exit 0
else
  phrase=$chosen_option;
fi

translation=$(sdcv --non-interactive --exact-search $phrase);
#chosen_option=$(echo -e "Copy\nClose" | sed 's/<[^>]*>//g' | rofi -dmenu -i -p "Translation" -mesg $translation);
chosen_option=$(echo -e "Close\nCopy\n$translation" | sed 's/<[^>]*>//g' | rofi -dmenu -i -p "Translation" -mesg "Select a line to copy.");

if [ -z "$chosen_option" ] || [ "$chosen_option" == "Close" ]; then
  exit 0
elif [ "$chosen_option" == "Copy" ]; then
  # FIXME Do not copy multiple-lined result to a single line
  echo $translation | xclip -in -selection clipboard;
else
  echo $chosen_option | xclip -in -selection clipboard;
fi

