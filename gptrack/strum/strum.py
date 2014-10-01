#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle as pickle
import os
import pylab as plt


class Strum():

    def __init__(self):
        self._left = np.array([])
        self._right = np.array([])

    def up_down(self):
        pass

    def append(self, pts):
        if self._left.any() and self._right.any():
            self._left = np.vstack((self._left, pts[0]))
            self._right = np.vstack((self._right, pts[1]))
        else:
            self._left, self._right = pts

    def plot(self, hand='right', coord=2):
        if self._pts.any():
            if hand == 'right':
                pts = self._right[:, coord]
                plt.plot(pts)
                plt.show()

    def save(self, fn):
        pickle.dump(self._pts, open(fn, 'w'))

    def load(self, fn):
        assert os.path.exists(fn)
        self._pts = pickle.load(open(fn, 'r'))


if __name__ == '__main__':
    pass
