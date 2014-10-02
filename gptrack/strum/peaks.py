#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from scipy.ndimage.filters import gaussian_filter1d


class FindPeaks():

    def __init__(self, slopeth, ampf, var, ngroup, debug=False):
        self._slth = slopeth
        self._ampf = ampf
        self._var = var
        self._w = np.round(ngroup/2 + 1)
        self._debug = debug

    def run(self, y):
        y = y - y.mean()
        d = self.__deriv(y)
        d = gaussian_filter1d(d, self._var) if self._var else d
        peaks = []
        peaks = self.__asd(y, d, peaks, lambda x, y: x < y)
        peaks = self.__asd(-y, d, peaks, lambda x, y: x > y)

        if self._debug:
            import pylab as plt
            plt.plot(y)
            plt.plot(peaks, y[peaks], 'o')
            plt.show()

        return peaks

    def __asd(self, y, d, peaks, f):
        N = len(d)-1
        AMP_TH = y.max()/2 * self._ampf

        for i in np.arange(0, N):
            if f(np.sign(d[i]), np.sign(d[i+1])):
                if f(d[i]-d[i+1], self._slth * y[i]):
                    if y[i] > AMP_TH or y[i+1] > AMP_TH:
                        #k = i-self._w if i-self._w > 0 else 0
                        #l = i+self._w if i+self._w < N else N
                        #yy = y[k:l]
                        peaks.append(i)
        return peaks

    def __deriv(self, x):
        d = np.zeros(x.shape)
        d[1:-1] = (np.roll(x, 1)[1: -1] - np.roll(x, -1)[1:-1]) / 2.
        d[0] = x[1] - x[0]
        d[-1] = x[-1] - x[-2]
        return d


if __name__ == '__main__':
    import cPickle as pickle

    pts = pickle.load(file('data/strokes/Am_r.pck'))
    y = pts[1][:, 1]

    fp = FindPeaks(0, 0.2, 10, 5, False)
    fp.run(y)
