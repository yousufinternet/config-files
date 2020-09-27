#!/usr/bin/env python

import os
import pypandoc
import subprocess as sp

path = os.path.expanduser('~/.config/sxhkd/sxhkdrc')
with open(path, 'r') as f_obj:
    sxhkdrc = f_obj.read()

result = []
for line in sxhkdrc.split('\n#'):
    line = line.strip().split('\n')
    if len(line) == 1:
        result.append(line[0])
    elif len(line) > 2:
        result.append(line[0])
        result.append('\n')
        binding = line[1].strip().replace('{', '\\{').replace('}', '\\}').replace('_', '\\_')
        binding = ' '.join(f'***{w}***' for w in binding.split())
        result.append(f'{binding}')
        result.append('```bash')
        result.append('\n'.join(f'   {l.strip()}' for l in line[2:]))
        result.append('```')
        result.append('\\vspace{12pt}')
    else:
        print(len(line))
        break

result_txt = '\n'.join(result)
print(result_txt)
with open('sxhkdrc_help.md', 'w+') as f_obj:
    f_obj.write('\n'.join(result))

output_report = pypandoc.convert_text(
    result_txt, to='pdf', format='md', outputfile='sxhkdrc_help.pdf',
    extra_args=('--toc', '-N'))

sp.Popen('zathura sxhkdrc_help.pdf', shell=True)
