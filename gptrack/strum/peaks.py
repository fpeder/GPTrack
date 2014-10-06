#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt

from scipy.ndimage.filters import gaussian_filter1d


class FindPeaks():

    def __init__(self, th, var, f):
        self._th = th
        self._var = var
        self._f = f
        self._y, self._p = None, None

    def run(self, y):
        self._y = y
        y = self.__smooth(y)

        def less(x, y):
            return x < y

        def greater(x, y):
            return x > y

        pos = self.__detect_peaks(y, less, greater, 1)
        neg = self.__detect_peaks(y, greater, less, -1)
        peaks = pos + neg

        self._p = peaks
        return peaks

    def __detect_peaks(self, y, f1, f2, sign):
        y = self.__normalize(y, 2)
        d = self.__smooth(self.__deriv(y))
        N = len(d)-1
        peaks = []

        for i in np.arange(0, N):
            if f1(np.sign(d[i]), np.sign(d[i+1])):
                strength = np.abs((d[i+1] - d[i-1])/2)

                if f2(y[i], sign * self._th):
                    peaks.append(i)
                elif strength > self._th:
                    peaks.append(i)
                else:
                    pass

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
    fp = FindPeaks(0.001, 10, 0.75)
    fp.run(y)
    fp.plot()
