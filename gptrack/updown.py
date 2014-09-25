#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class UpDown():

    def __init__(self, miss=-1):
        self._pts, self._nframe = None, None
        self._miss = miss

    def run(self, pts):
        self._pts = pts
        self._nframe = np.arange(len(pts))

        self.__remove_non_detect()

        y = self._pts[:, 3]
        df = np.diff(y)
        th = np.abs(df.max() - df.min())*0.75/2
        sign = np.sign(df)

        ud = sign.copy()
        ud[np.abs(df) < th] = 0
        return (ud, self._nframe)

    def __remove_non_detect(self):
        idx = ((pts[:, 1] != self._miss) & (pts[:, 2] != self._miss) &
               (pts[:, 2] != self._miss) & (pts[:, 3] != self._miss))
        self._pts = self._pts[idx, :]
        self._nframe = self._nframe[idx]

    def __get_right_hand(self):
        return self._pts[:, 2:4]


if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="pickle sequence of points")
    parser.add_argument("-o", "--outfile", type=str, required=True,
                        help="up and down sequence")
    args = parser.parse_args()

    pts = pickle.load(open(args.infile, 'r'))
    ud = UpDown()
    udseq = ud.run(pts)

    if args.outfile:
        pickle.dump(udseq, open(args.outfile, 'w'))
