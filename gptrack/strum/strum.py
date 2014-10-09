#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle as pickle
import os
import sys


class Strum():

    def __init__(self, miss=-1):
        self._miss = -1
        self._right = np.array([])

    def append(self, pts):
        if self.__have_pts():
            self._right = np.vstack((self._right, pts[1]))
        else:
            self._right = pts[1]

    def save(self, fn):
        if self.__have_pts():
            pickle.dump(self._right, open(fn, 'w'))
        else:
            sys.stderr.write('err: strum.py: no pts')

    def load(self, fn):
        assert os.path.exists(fn)
        tmp = pickle.load(open(fn, 'r'))
        self._right = tmp[1] if len(tmp) == 2 else tmp

    def __have_pts(self):
        return self._right.any()

    @property
    def right(self):
        return self._right


if __name__ == '__main__':
    pass
