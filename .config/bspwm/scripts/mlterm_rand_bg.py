#!/usr/bin/env python
'Start mlterm with a random bg hue, similar to konsole random color feature'
import sys
import random
from colour import Color
from wmutils.processes import cmd_run


def randomize_hue(bg_hex):
    color_obj = Color(bg_hex)
    randomized = random.random()
    color_obj.hue = randomized
    sat = color_obj.saturation
    color_obj.saturation = sat+randomized if (sat+randomized) <= 0.8 else 0.8
    return color_obj.get_hex()


def main(bg_hex, trans):
    bg_hex = randomize_hue(bg_hex) + trans
    cmd_run(f"mlterm --bg '{bg_hex}' "+' '.join(sys.argv[1:]))


if __name__ == '__main__':
    bg_hex = '#282A36'
    trans = 'ae'
    main(bg_hex, trans)
