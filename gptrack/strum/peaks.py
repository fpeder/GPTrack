#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt


class Peaks():
    def __init__(self, k=10, h=3):
        self._k = k
        self._h = h
        self._peaks = np.array([])

    def run(self, sig):
        a = [self.__s1(sig, i) for i in range(len(sig))]
        m, s = a[a > 0].mean(), a[a > 0].std()

        O = [[x, i] for i, x in enumerate(a) if x > 0 and (x-m) > (self._h*s)]

        for i in np.arange(len(O)):
            for j in np.arange(i+1, i+self._k+1):
                if j < len(O):
                    if O[i][0] < O[j][0]:
                        O[i][0] = -1
                    else:
                        O[j][0] = -1

        O = np.array(O)
        self._peaks = O[O[:, 0] != -1][:, 1].astype(np.int32)
        return self._peaks

    def __s1(self, x, i):
        idx = np.arange(i-self._k, i)
        idx = idx[idx >= 0]
        max1 = (x[idx] - x[i]).max() if idx.any() else 0

        idx = np.arange(i+1, i+self._k+1)
        idx = idx[idx < len(x)]
        max2 = (x[idx] - x[i]).max() if idx.any() else 0

        return (max1 + max2)/2

    def plot(self, sig):
        if self._peaks.any():
            plt.plot(sig)
            plt.plot(self._peaks, sig[self._peaks], 'o')
            plt.show()


if __name__ == '__main__':
    x = np.random.rand(100)
    x[10] = 10
    x[50] = 15

    p = Peaks()
    p.run(x)
    p.plot(x)
