#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle

if __name__ == '__main__':
    import sys
    import pylab as plt
    import os

    fn = sys.argv[1]
    ud, frame = pickle.load(open(fn, 'r'))

    plt.plot(frame, ud)
    plt.title(os.path.basename(fn))
    plt.xlabel("frame")
    plt.ylabel("stroke")
    plt.savefig(fn + '.png')
