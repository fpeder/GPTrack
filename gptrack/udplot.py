#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle

if __name__ == '__main__':
    import sys
    import pylab as plt

    ud, frame = pickle.load(open(sys.argv[1], 'r'))
    plt.plot(frame, ud)
    plt.show()
