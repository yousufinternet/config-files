#!/usr/bin/env python

import os
import sys
import shlex
import subprocess as sp


def get_text():
    current_mode = os.getenv('QUTE_MODE')
    if current_mode == 'hints':
        text = os.getenv('QUTE_SELECTED_TEXT')
    elif current_mode == 'commands':
        text_path = os.getenv('QUTE_TEXT')
        if text_path and os.path.exists(text_path):
            with open(text_path, 'r') as f:
                text = f.read()
        else:
            text = 'No text found'
        print(text)
    return text

def create_tts_sound(text):
    text = shlex.quote(text)
    P = sp.Popen('pico2wave --wave=.qutereader_temp.wav '+text,
                    shell=True, text=True)
    P.wait()
    if os.path.exists('.qutereader_temp.wav'):
        return True
    return


def main():
    text = get_text()
    create_tts_sound(text)
    temp_Audio = os.path.abspath('.qutereader_temp.wav')
    P = sp.Popen(['tsp', 'play', temp_audio])
    os.remove(temp_audio)
    
if __name__ == '__main__':
    main()
