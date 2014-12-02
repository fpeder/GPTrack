#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import numpy as np
import cPickle as pickle


class Loader():

    def __init__(self, path, prefix=['gt.', 'ud.'], ext=['.pck']):
        self._path = path
        self._pref = prefix
        self._ext = ext

    def run(self, chord):
        asd = []
        for pref in self._pref:
            tmp = os.path.join(self._path, pref + chord + self._ext)
            assert os.path.exists(tmp), '! file...'
            tmp = pickle.load(open(tmp, 'r'))
            asd.append(tmp)
        return asd[0], asd[1]


class PErr():

    def __init__(self, path='data/strokes', prefix=['gt.', 'ud.'],
                 ext='.pck'):
        self._loader = Loader(path, prefix, ext)

    def run(self, chord):
        gt, ud = self._loader.run(chord)
        idx, w = self.__get_window(gt)
        ud = ud[0]

        # import pylab as plt
        # for i in idx:
        #     plt.plot(ud)
        #     plt.plot(i, gt[i], 'ro', markersize=8)
        #     plt.ylim(-1.2, 1.2)
        #     plt.axvline(x=i-w, ymin=-1, ymax=1, color='g')
        #     plt.axvline(x=i+w, ymin=-1, ymax=1, color='g')
        #     plt.plot((i-w, i+w), (gt[i], gt[i]), color='g')
        #     plt.show()

        res = sum([sum(ud[i-w: i+w] == gt[i]) == 1 for i in idx])
        return (1 - res.astype(np.float)/len(idx)) * 100

    def __get_window(self, gt):
        idx = np.where(gt != 0)[0]
        w = np.diff(idx).mean()
        return idx, w/2


if __name__ == '__main__':
    import sys

    perr = PErr()
    print perr.run(sys.argv[1])
