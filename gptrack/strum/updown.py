#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from peaks import FindPeaks


class UpDown():

    def __init__(self, slth, var, f, miss=-1):
        self._pts, self._nframe = None, None
        self._miss = miss
        self._pd = FindPeaks(slth, var, f)

    def run(self, pts):
        self._pts = pts[1] if len(pts) == 2 else pts
        self._nframe = np.arange(self._pts.shape[0])
        self.__remove_non_detect()

        y = self._pts[:, 1]
        y = y - y.mean()

        peaks = self._pd.run(y)
        ud = np.zeros(y.shape)
        ud[peaks] = np.sign(y[peaks])

        return ud, self._nframe

    def __remove_non_detect(self):
        idx = ((self._pts[:, 0] != self._miss) &
               (self._pts[:, 1] != self._miss))
        self._pts = self._pts[idx, :]
        self._nframe = self._nframe[idx]


if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="pickle sequence of points")
    parser.add_argument("-o", "--outfile", type=str,
                        help="up and down sequence")
    args = parser.parse_args()

    pts = pickle.load(open(args.infile, 'r'))
    ud = UpDown(0.001, 10, .75)
    udseq = ud.run(pts)

    if args.outfile:
        pickle.dump(udseq, open(args.outfile, 'w'))
