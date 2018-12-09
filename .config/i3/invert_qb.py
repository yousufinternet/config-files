#!/usr/bin/env python
import subprocess
import os
import psutil
import posixpath

def main():
    prefix_path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    with open(os.path.join(prefix_path, 'color_rgb_shift_bias.glsl'), 'r') as f_obj:
        color_matrix = f_obj.read()

    if not os.path.exists(os.path.join(prefix_path, '.qb_invert_status')):
        with open(os.path.join(prefix_path, '.qb_invert_status'), 'w+') as f_obj:
            f_obj.write('True')
        subprocess.Popen(['compton', '--backend', 'glx', '--glx-fshader-win', color_matrix, '--invert-color-include', 'class_g="qutebrowser"'])

    with open(os.path.join(prefix_path, '.qb_invert_status'), 'r') as f_obj:
        if f_obj.read() == 'True':
            qb_status = True
        else:
            qb_status = False

    if qb_status:
        with open(os.path.join(prefix_path, '.qb_invert_status'), 'w') as f_obj:
            f_obj.write('False')
        for process in psutil.process_iter():
            if 'compton' in process.cmdline():
                process.terminate()
                break
        subprocess.Popen(['compton'])
        print('after subprocess')
    else:
        with open(os.path.join(prefix_path, '.qb_invert_status'), 'w') as f_obj:
            f_obj.write('True')
        for process in psutil.process_iter():
            if 'compton' in process.cmdline():
                process.terminate()
                break
        subprocess.Popen(['compton', '--backend', 'glx', '--glx-fshader-win', color_matrix, '--invert-color-include', 'class_g="qutebrowser"'])


if __name__ == '__main__':
    main()
