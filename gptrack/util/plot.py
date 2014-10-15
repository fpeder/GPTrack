#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle

if __name__ == '__main__':
    import sys
    import pylab as plt
    import os

    fn = sys.argv[1]
    ud, frame = pickle.load(open(fn, 'r'))
    asd, = plt.plot(frame, ud)
    plt.title(os.path.basename(fn))

    gt = fn.replace('ud.', 'gt.')
    if os.path.exists(gt):
        udgt = pickle.load(open(gt, 'r'))
        qwe, = plt.plot(frame[udgt != 0], udgt[udgt != 0], 'ro')

    plt.ylim([-1.1, 1.1])
    plt.xlabel('frame')
    plt.ylabel('stroke')
    plt.legend([asd, qwe], ['my', 'gt'])
    plt.savefig(fn + '.png')
