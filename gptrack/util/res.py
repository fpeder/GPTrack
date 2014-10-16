#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle as pickle
import os


class PErr():
    UP = 1
    DOWN = -1

    def __init__(self, w=None, s=1):
        self._w = w
        self._s = s

    def run(self, my, gt):
        self.__estimate_width(gt)
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

    def __estimate_width(self, x):
        idx = np.where(x != 0)[0]
        w = np.sort(np.diff(idx))
        self._w = w[0] / self._s


class Results():
    MY = 'ud'
    GT = 'gt'
    EXT = '.pck'

    def __init__(self, path, chords, speed, fps, w=75):
        self._path, self._chords, self._speed = path, chords, speed
        self._fps = fps
        self._pe = PErr()
        self._res = None

    def run(self):
        res = {}
        for fps in self._fps:
            res['fps'] = fps
            for ch in self._chors:
                for sp in self._speed:
                    name = '.' + ch + '_' + sp
                    pe = self.__prob_of_error(name)
                    res['fps'][name] = pe
        self._res = res

    def __prob_of_error(self, base):
        my, gt = self.__load(base)
        return self._pe.run(my, gt)

    def __load(self, base):
        base = base + self.EXT
        my = os.path.join(self._path, self.MY + base)
        gt = os.path.join(self._path, self.GT + base)
        my, frame = pickle.load(open(my, 'r'))
        gt = pickle.load(open(gt, 'r'))
        return my, gt

    # def __repr__(self):
    #     res = ''
    #     if self._res:
    #         res += '---' + self._fps + '---\n'
    #         for ch in self._chords:
    #             for sp in self._speed:
    #                 name = ch + '_' + sp
    #                 res += name + ' ' + str(self._res[ch + '_' + sp][-1])
    #                 res += '\n'
    #     return res

    # def to_latex(self):
    #     res = ''
    #     if self._res:
    #         for ch in self._chords:
    #             res += '\multicolumn{3}{*}{' + str(ch) + '}'
    #             for sp in ['s', 'n', 'r']:
    #                 name = ch + '_' + sp
    #                 pe = np.round(self._res[name][1], decimals=2)
    #                 res += '& ' + str(pe)
    #             res += '\\\\\ \n'
    #     return res


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--stroke', type=str, required=True)
    parser.add_argument('-f', '--fps', type=str, required=True)
    args = parser.parse_args()

    path, fps = args.stroke, args.fps
    assert os.path.exists(path), 'path'

    res = Results(path, ['Am', 'E', 'G'], ['s', 'r', 'n'], fps)
    res.run()
    print res.to_latex()
