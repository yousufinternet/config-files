#! /usr/bin/env python3

import os
import re
import subprocess

man_pages = subprocess.check_output('man -k .', text=True, shell=True)

with open('.temp_list', 'w+') as f_obj:
    f_obj.write(man_pages)
P = subprocess.Popen(f'cat .temp_list | rofi -matching regex -filter "^" -dmenu',
                     text=True, shell=True, stdout=subprocess.PIPE)
P.wait()
man_page = P.stdout.read().strip()
print(man_page)
man_page = re.search(r'(.*?)\((.*?)\).*', man_page)
man_page = f'{man_page.group(2)} {man_page.group(1).strip()}'
print(man_page)
subprocess.Popen(f'man -Tpdf {man_page} | zathura -', text=True, shell=True)

os.remove('.temp_list')
