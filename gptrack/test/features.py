#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import ctypes as ct

from util import makeCallableString


class BlockHistInterface():

    def __init__(self, w, s, nbins, ndim):
        self._w = w
        self._s = s
        self._nbins = nbins
        self._ndim = ndim
        self._blockproc = np.ctypeslib.load_library('blockProc', '.')

    def run(self, img):
        img = np.int32(img)
        M, N, nch = img.shape
        R, C = self.__new_dims(M, N)
        X = np.zeros((R, C), np.int32)

        args = [ct.POINTER(ct.c_int), ct.c_int, ct.c_int, ct.c_int,
                ct.POINTER(ct.c_int), ct.c_int, ct.c_int,
                ct.c_int, ct.c_int, ct.c_int]

        self._blockproc.hist.argtypes = args
        self._blockproc.hist.restype = ct.c_int
        self._blockproc.hist(img.ctypes.data_as(ct.POINTER(ct.c_int)),
                             M, N, nch,
                             X.ctypes.data_as(ct.POINTER(ct.c_int)), R, C,
                             self._w, self._s, self._nbins)
        return X

    def __new_dims(self, M, N):
        R = np.int32(np.ceil((M - self._w)/self._s) *
                     np.ceil((N - self._w)/self._s))
        C = self._nbins * self._ndim
        return R, C


class Features():

    def __init__(self, featspec):
        self._bs = featspec['blocksize']
        self._skip = featspec['skip']
        self._kind = featspec['kind']

    def run(self, img, gt=np.array([])):
        X = np.hstack([self.__run(img, k) for k in self._kind])
        if gt.any():
            s = self._skip
            w = self._bs
            M, N = gt.shape
            gt = gt[0:M-w:s, 0:N-w:s]
            gt = gt.reshape(-1)
        return X, gt

    def __run(self, img, kind):
        X = []
        method = kind[0]
        if method == 'Hist':
            nbins = kind[1]['nbins']
            nch = img.shape[2]
            bhi = BlockHistInterface(self._bs, self._skip, nbins, nch)
            X = bhi.run(img)
        return X

    #def __parse(self, desc):
    #    tmp = makeCallableString(desc)
    #    return eval(tmp)

    @property
    def skip(self):
        return self._skip

    @property
    def bs(self):
        return self._bs


if __name__ == '__main__':
    img = cv2.imread('db/2.jpg')
    gt = cv2.imread('db/gt.2.png')
    desc = {'blocksize': 8, 'skip': 1, 'kind': [['Hist', {'nbins': 16}]]}

    feat = Features(desc)
    X, y = feat.run(img, gt)

