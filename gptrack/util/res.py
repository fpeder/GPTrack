#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from perr import PErr

if __name__ == '__main__':
    chord = ['Am0', 'Am7', 'Bm7', 'C0', 'C7', 'E0', 'G0', 'G7']
    speed = ['s', 'n', 'r']
    perr = PErr()

    res = []
    for ch in chord:
        pr = [perr.run(ch + '_' + s) for s in speed]
        print ch, pr
        res.append(pr)

    print np.array(res).mean(axis=0)
