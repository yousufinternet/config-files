#!/usr/bin/env python

import os
import sys
import shlex
import tempfile
import subprocess as sp


def get_text():
    current_mode = os.getenv('QUTE_MODE')
    text = 'No text found'
    if current_mode == 'hints':
        text = os.getenv('QUTE_SELECTED_TEXT')
    elif current_mode == 'command':
        text_path = os.getenv('QUTE_TEXT')
        if text_path and os.path.exists(text_path):
            with open(text_path, 'r') as f:
                text = f.read()
    print(text)
    return text


def create_tts_sound(text):
    text = shlex.quote(text)
    tmp = tempfile.NamedTemporaryFile()
    tmpfn = tmp.name
    print(tmpfn)
    P = sp.Popen(f'pico2wave --wave={tmpfn}.wav {text}',
                 shell=True, text=True)
    P.wait()
    if os.path.exists(tmpfn+'.wav'):
        return tmpfn+'.wav'
    return


def main():
    text = get_text()
    tmpfn = create_tts_sound(text)
    if tmpfn:
        sp.Popen(['tsp', 'play', tmpfn])
        sp.Popen(['tsp', 'rm', tmpfn])


if __name__ == '__main__':
    main()
