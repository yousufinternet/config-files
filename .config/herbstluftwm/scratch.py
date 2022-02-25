#!/usr/bin/env python
# Scratchpads for herbstluftwm

import re
import argparse
import subprocess as sp


def hc(*args):
    P = sp.Popen(
        f'herbstclient {" ".join(args)}', text=True, shell=True,
        stdout=sp.PIPE, stderr=sp.PIPE)
    err = not bool(P.stderr.read())
    out = P.stdout.read()
    return out, err


def get_class(wid):
    '''
    get passed window id class using xprop output
    '''
    try:
        out = sp.check_output(
            f'xprop -id {wid} WM_CLASS', text=True, shell=True).strip()
        wm_class = [wid.strip('"') for wid in out.split(' = ')[1].split(', ')]
        return wm_class
    except Exception:
        return []

# def get_class(wid):
#     '''
#     get passed window id instance and class
#     '''
#     try:
#         instance = hc(f'get_attr clients.{wid}.instance')[0]
#         wclass = hc(f'get_attr clients.{wid}.class')[0]
#         return wclass.strip(), instance.strip()
#     except Exception:
#         return None, None


def float_lt_zero(num):
    try:
        num = float(num)
    except ValueError:
        raise argparse.ArgumentError(f'Invalid {num} cannot convert to float')
    if num < 0:
        raise argparse.ArgumentError(f'{num} should not be less than 0')
    return num


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--termclass',
                        help='pass a class name for mlterm instance')
    parser.add_argument('-w', '--width', dest='width', default=0.5,
                        type=float_lt_zero, nargs='?',
                        help=('width in percent (pixels if more than 1) for'
                              ' the dropdown window'))
    parser.add_argument('-ht', '--height', dest='height', default=0.5,
                        type=float_lt_zero, nargs='?',
                        help=('height in percent for'
                              ' the dropdown window'))
    parser.add_argument('-x', default=0, type=float_lt_zero)
    parser.add_argument('-y', default=0, type=float_lt_zero)
    parser.add_argument('--termflags', nargs=argparse.REMAINDER)
    return parser.parse_args()


def ishidden(wid):
    return eval(hc(f'attr clients.{wid}.minimized')[0].title())


def win_exists(term_class):
    clients = [wid.rstrip('.') for wid in
               hc('attr clients')[0].split() if wid.startswith('0x')]
    for wid in clients:
        if term_class == get_class(wid)[1]:
            return wid
    return False


def win_geometry(wid):
    '''
    given a window id return geometry using xwininfo package
    (x_pos, y_pos, width, height) dictionary
    '''
    window_geometry = ' '.join(
        sp.check_output(f'xwininfo -metric -shape -id {wid}',
                        text=True, shell=True).strip().split('\n')[2:8])
    regex_obj = re.search(
        r'Abs.*X.*?(-?\d+).*Abs.*Y.*?(-?\d+).*Width:\s+(\d+).*Height:\s+(\d+)',
        window_geometry)
    window_geometry = {
        'x_pos': int(regex_obj.group(1)),
        'y_pos': int(regex_obj.group(2)),
        'width': int(regex_obj.group(3)),
        'height': int(regex_obj.group(4))
    }
    return window_geometry


def screen_dim():
    screen_dims = hc('monitor_rect')[0].split()
    return {'x': int(screen_dims[0]), 'y': int(screen_dims[1]),
            'width': int(screen_dims[2]), 'height': int(screen_dims[3])}


def create_geometry_str(x, y, w, h):
    screen_dims = screen_dim()
    if x <= 1:
        x *= screen_dims['width']
        x += screen_dims['x']
    if y <= 1:
        y *= screen_dims['height']
        y += screen_dims['y']
    if w <= 1:
        w *= screen_dims['width']
    if h <= 1:
        h *= screen_dims['height']
    return f'{w:0.0f}x{h:0.0f}{x:+0.0f}{y:+0.0f}'


def repair_geometry(wid, gmt):
    current = win_geometry(wid)
    print(current)
    screen_dims = screen_dim()
    print(screen_dims)
    re_obj = re.match(r'(\d+)x(\d+)([+-]\d+)([+-]\d+)', gmt)
    w, h, x, y = (float(re_obj.group(i)) for i in range(1,5))
    print(w, h, x, y)
    x = x+screen_dims['width'] if x < 0 else x
    y = y+screen_dims['height'] if y < 0 else y
    if w != current['width']:
        sp.Popen(f'xdo resize -w {w} {wid}', shell=True)
    if h != current['height']:
        sp.Popen(f'xdo resize -h {h} {wid}', shell=True)
    if x != current['x_pos'] or y != current['y_pos']:
        sp.Popen(f'xdo move -y {y} -x {x} {wid}', shell=True)


def start_terminal(termclass, termargs):
    P = sp.Popen('herbstclient --idle focus_changed', text=True, shell=True, stdout=sp.PIPE)
    print(termargs)
    sp.Popen('konsole '+(' '.join(termargs) if termargs else ''),
             shell=True, text=True)
    wid = P.stdout.readline().strip().split()[1]
    sp.Popen(f'xdotool set_window --class "{termclass}" {wid}', shell=True, text=True)
    P.kill()


def toggle_hide(wid):
    'toggle the hidden flag of the passed node'
    if ishidden(wid):
        hc(f'set_attr clients.{wid}.minimized false')
        hc(f'bring {wid}')
    else:
        hc(f'set_attr clients.{wid}.minimized true')


def reapply_rules(term_class, geometry):
    dropdown_rules = 'floating=on floatplacement=none '
    dropdown_rules += f'floating_geometry={geometry}'
    rules_reg = r'\s*'.join(dropdown_rules.split())
    full_reg = r'.*class='+term_class+rules_reg+r'.*'
    rules = hc('list_rules')[0].split('\n')
    drop_rules = [rule for rule in rules if re.match(full_reg, rule)]
    if not drop_rules:
        hc(f'rule class={term_class} {dropdown_rules}')


def main():
    args = parse_args()
    geometry = create_geometry_str(args.x, args.y, args.width, args.height)
    wid = win_exists(args.termclass)
    if not wid:
        reapply_rules(args.termclass, geometry)
        start_terminal(args.termclass, args.termflags)
    else:
        toggle_hide(wid)
        repair_geometry(wid, geometry)


if __name__ == '__main__':
    main()
