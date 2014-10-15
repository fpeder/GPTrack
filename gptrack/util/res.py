#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle as pickle
import os


class PErr():
    UP = 1
    DOWN = -1

    def __init__(self, w):
        self._w = w

    def run(self, my, gt):
        u = np.where(gt == self.UP)[0]
        d = np.where(gt == self.DOWN)[0]
        myu = self.__check(my, u, self.UP)
        myd = self.__check(my, d, self.DOWN)
        peu = self.__toPerr(myu, len(u))
        ped = self.__toPerr(myd, len(d))

        return peu, ped, (peu + ped)/2

    def __toPerr(self, x, n):
        return (1 - float(x)/n)*100

    def __check(self, my, idx, val):
        N, count = len(my), 0
        for i in idx:
            s = i-self._w/2 if i-self._w/2 > 0 else 0
            e = i+self._w/2 if i+self._w/2 < N else N
            tmp = my[s:e]

            if len(tmp[tmp == val]) == 1:
                count += 1
        return count


class Results():
    MY = 'ud'
    GT = 'gt'

    def __init__(self, path, chords, speed, w=75):
        assert os.path.exists(path), 'path doesn\'t exist'
        self._path = path
        self._chords = chords
        self._speed = speed
        self._pe = PErr(w)

    def run(self):
        res = []
        for ch in self._chords:
            for sp in self._speed:
                base = '.' + ch + '_' + sp + '.pck'
                my = os.path.join(self._path, self.MY + base)
                gt = os.path.join(self._path, self.GT + base)
                my, frame = pickle.load(open(my, 'r'))
                gt = pickle.load(open(gt, 'r'))
                res.append(self._pe.run(my, gt))

        return res


if __name__ == '__main__':
    res = Results('data/strokes', ['Am', 'E', 'G'], ['s', 'r', 'n'])
    r = res.run()
