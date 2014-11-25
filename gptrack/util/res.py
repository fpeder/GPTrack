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
    SEP = '_'

    def __init__(self, path, chords, speed, fps, w=75):
        self._path = path
        self._names = [c + '_' + s for c in chords for s in speed]
        self._fps = fps
        self._pe = PErr()
        self._res = None

    def run(self):
        res = {}
        for fps in self._fps:
            res[str(fps)] = {}
            path = os.path.join(self._path, str(fps))
            for x in self._names:
                res[str(fps)][x] = self.__prob_of_error(path, x)
        self._res = res

    def __prob_of_error(self, path, base):
        my, gt = self.__load(path, base)
        return self._pe.run(my, gt)

    def __load(self, path, base):
        base = '.' + base + self.EXT
        my = os.path.join(path, self.MY + base)
        gt = os.path.join(path, self.GT + base)
        my, frame = pickle.load(open(my, 'r'))
        gt = pickle.load(open(gt, 'r'))
        return my, gt

    def __repr__(self):
        r, res = self._res, ''
        for key in r.keys():
            res += '--- ' + key + ' ---\n'
            for name in self._names:
                pe = np.round(r[key][name][-1], decimals=2)
                res += name + ' ' + str(pe) + '\n'
        return res

    def to_latex(self):
        res = ''
        for fps in self._fps:
            res += '\\multirow{3}{*}{' + str(fps) + '} '
            chords = list(set([x.split(self.SEP)[0] for x in self._names]))
            num = len(self._names)
            nspeed = num/len(chords)
            asd = [self._names[i:i+nspeed] for i in range(0, num, nspeed)]
            curr = self._res[str(fps)]
            for i, x in enumerate(asd):
                res += '& ' + chords[i]
                tmp = [str(np.round(curr[i][-1], decimals=2)) for i in x]
                res += ' & ' + ' & '.join(tmp)
                res += '\\\\ \n'
            res += '\midrule \n'
        return res


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--stroke', type=str, required=True)
    parser.add_argument('-f', '--fps', type=str, required=True)
    args = parser.parse_args()

    path, fps = args.stroke, args.fps
    assert os.path.exists(path), 'path'

    res = Results(path, ['Am', 'E', 'G'], ['s', 'n', 'r'], [])
    res.run()

    print res.to_latex()
