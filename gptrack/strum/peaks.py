#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt

from scipy.ndimage.filters import gaussian_filter1d


def less(x, y):
    return x < y


def greater(x, y):
    return x > y


class FindPeaks():

    def __init__(self, th, var, f):
        self._th = th
        self._var = var
        self._f = f
        self._y, self._p = None, None

    def run(self, y):
        y = self.__normalize(self.__smooth(y), 2)
        self._y = y
        return self.__detect_peaks(y)

    def __detect_peaks(self, y):
        d = self.__smooth(self.__deriv(y))
        sgn = np.sign(d)
        peaks = np.zeros(len(d))

        prev = 0
        for i in np.arange(0, len(d) - 1):

            if sgn[i] != sgn[i+1]:
                curr = y[i]

                if np.abs((d[i] - d[i+1])/2) > self._th:
                    peaks[i] = sgn[i]

                if np.abs(y[i]) > self._f and np.abs(curr-prev) > .2:
                    peaks[i] = sgn[i]

                prev = curr

        return peaks

    def __smooth(self, x):
        x = gaussian_filter1d(x, self._var) if self._var else x
        return x

    def plot(self):
        plt.plot(self._y)
        plt.plot(self._p, self._y[self._p], 'o')
        plt.show()

    def __normalize(self, x, m):
        x = x - x.min()
        x = x/x.max() * m
        x = x - m/2
        return x

    def __deriv(self, x):
        d = np.zeros(x.shape)
        d[1:-1] = (np.roll(x, 1)[1: -1] - np.roll(x, -1)[1:-1]) / 2.
        d[0] = x[1] - x[0]
        d[-1] = x[-1] - x[-2]
        return d

1
if __name__ == '__main__':
    import cPickle as pickle
    import sys

    pts = pickle.load(file(sys.argv[1]))
    y = pts[1][:, 1]
    fp = FindPeaks(0.001, 20, 0.75)
    fp.run(y)
    fp.plot()
