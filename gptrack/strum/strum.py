#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle as pickle
import os


class Strum():

    def __init__(self, miss=-1):
        self._miss = -1
        self._left = np.array([])
        self._right = np.array([])

    def append(self, pts):
        if self.__have_pts():
            self._left = np.vstack((self._left, pts[0]))
            self._right = np.vstack((self._right, pts[1]))
        else:
            self._left, self._right = pts[0], pts[1]

    def save(self, fn):
        if self.__have_pts():
            pickle.dump((self._left, self._right), open(fn, 'w'))

    def load(self, fn):
        assert os.path.exists(fn)
        self._left, self._right = pickle.load(open(fn, 'r'))

    def __have_pts(self):
        return self._left.any() and self._right.any()

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


if __name__ == '__main__':
    pass
