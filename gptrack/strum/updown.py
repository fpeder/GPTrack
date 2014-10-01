#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt

from scipy.signal import find_peaks_cwt


class UpDown():

    def __init__(self, miss=-1, f=2.5, fth=0.75, lh=7, lcwt=25):
        self._pts, self._nframe = None, None
        self._f, self._fth = f, fth
        self._miss = miss
        self._lcwt = np.arange(1, lcwt)
        self._h = 1./lh * np.ones(lh) if lh else np.array([])

    def run(self, pts):
        self._pts = pts
        self._nframe = np.arange(len(pts))
        self.__remove_non_detect()

        y = pts[:, 3]
        if self._h.any():
            y = np.convolve(y, self._h, 'same')

        df = np.diff(y)
        if self._h.any():
            df = np.convolve(df, self._h, 'same')

        ustk = find_peaks_cwt(df, self._lcwt)
        dstk = find_peaks_cwt(-df, self._lcwt)
        ustk, dstk = self.__remove_outliers(df, ustk, dstk)

        updown = np.zeros(len(df), np.int32)
        updown[ustk] = 1
        updown[dstk] = -1
        return updown, self._nframe[0:-1]

    def __remove_outliers(self, df, ustk, dstk):
        mu = df[ustk].mean()
        md = df[dstk].mean()
        ustk = [x for x in ustk if df[x] > 0.6*mu]
        dstk = [x for x in dstk if df[x] < 0.6*md]
        return ustk, dstk

    def __remove_non_detect(self):
        idx = ((pts[:, 1] != self._miss) & (pts[:, 2] != self._miss) &
               (pts[:, 2] != self._miss) & (pts[:, 3] != self._miss))
        self._pts = self._pts[idx, :]
        self._nframe = self._nframe[idx]

    # def run_old(self, pts):
    #     self._pts = pts
    #     self._nframe = np.arange(len(pts))
    #     self.__remove_non_detect()

    #     y = pts[:, 3]
    #     if self._h.any():
    #         y = np.convolve(y, self._h, 'same')
    #     y = y - y.mean()

    #     ud = self.__detect_updown(y)
    #     ud = self.__simplify(ud)

    #     return ud, self._nframe[0:-1]

    # def __detect_updown(self, y):
    #     sign = -np.sign(y)
    #     df = np.diff(y)
    #     df = np.convolve(y, self._h, 'same')
    #     th = self.__find_thresh(df)

    #     ud = df.copy()
    #     ud[np.abs(df) < th] = 0
    #     ud[np.abs(df) > 0] = 1
    #     ud *= sign[0:-1]

    #     import pdb; pdb.set_trace()

    #     return ud

    # def __simplify(self, ud):
    #     i = 0
    #     while i < len(ud):
    #         j = i+1
    #         if j >= len(ud):
    #             break
    #         while ud[i] == ud[j]:
    #             ud[j] = 0
    #             j += 1
    #             if j >= len(ud):
    #                 break
    #         i = j
    #         if i >= len(ud):
    #             break
    #     return ud

    # def __find_thresh(self, df):
    #     dev = np.sqrt(df.var())
    #     pos = df > self._f * dev
    #     neg = df < -self._f * dev
    #     th = (df[pos].mean() - df[neg].mean()) * self._fth/2
    #     #from scipy.signal import find_peaks_cwt
    #     #posdf = df[df > 0]
    #     #peaks = find_peaks_cwt(df, np.arange(1,25))
    #     #pth = df[peaks] 
    #     return th




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
