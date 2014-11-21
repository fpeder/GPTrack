#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import ctypes as ct

LIB = 'hands/skin/blockProc'


class BlockInterface(object):

    def __init__(self, w, s):
        self._w = w
        self._s = s
        self._blockproc = np.ctypeslib.load_library(LIB, '.')

    def __num_rows(self, M, N):
        R = np.int32(np.ceil((M - self._w)/self._s) *
                     np.ceil((N - self._w)/self._s))
        return R

    def setup(self, img, l):
        M, N, nch = img.shape
        R, C = self.__num_rows(M, N), l
        X = np.zeros((R, C), np.int32)
        return M, N, nch, X, R, C


class BlockHistInterface(BlockInterface):

    def __init__(self, w, s, nbins, ndim):
        BlockInterface.__init__(self, w, s)
        self._nbins = nbins
        self._ndim = ndim
        self._l = self._nbins * self._ndim

    def run(self, img):
        img = img.astype(np.int32)
        M, N, nch, X, R, C = self.setup(img, self._l)

        args = [ct.POINTER(ct.c_int), ct.c_int, ct.c_int, ct.c_int,
                ct.POINTER(ct.c_float), ct.c_int, ct.c_int,
                ct.c_int, ct.c_int, ct.c_int]

        self._blockproc.hist.argtypes = args
        self._blockproc.hist.restype = ct.c_int
        self._blockproc.hist(img.ctypes.data_as(ct.POINTER(ct.c_int)),
                             M, N, nch,
                             X.ctypes.data_as(ct.POINTER(ct.c_float)), R, C,
                             self._w, self._s, self._nbins)
        return X


class BlockGradientInterface(BlockInterface):

    def __init__(self, w, s, nch=3):
        BlockInterface.__init__(self, w, s)
        self._l = nch

    def run(self, img):
        M, N, nch, X, R, C = self.setup(img, self._l)
        img = self.__my_gradient(img)

        X = X.astype(np.float32)
        
        args = [ct.POINTER(ct.c_int), ct.c_int, ct.c_int, ct.c_int,
                ct.POINTER(ct.c_int), ct.c_int, ct.c_int,
                ct.c_int, ct.c_int]

        self._blockproc.gradient.argtypes = args
        self._blockproc.gradient.restype = ct.c_int
        self._blockproc.gradient(img.ctypes.data_as(ct.POINTER(ct.c_int)),
                                 M, N, nch,
                                 X.ctypes.data_as(ct.POINTER(ct.c_int)), R, C,
                                 self._w, self._s)
        return X

    def __my_gradient(self, img):
        img = img.astype(np.float32)

        def asd(img):
            dx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
            dy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
            rho = np.sqrt(dx**2 + dy**2)
            return rho

        tmp = [asd(img[:, :, i]) for i in range(3)]
        grad = np.dstack(tmp)
        return grad


class Features():

    def __init__(self, featspec):
        self._bs = featspec['blocksize']
        self._skip = featspec['skip']
        self._kind = featspec['kind']

    def run(self, img, gt=np.array([])):
        X = np.hstack([self.__run(img, k) for k in self._kind])
        if gt.any():
            s, w = self._skip, self._bs
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

        elif method == 'Gradient':
            bgi = BlockGradientInterface(self._bs, self._skip)
            X = bgi.run(img)

        else:
            pass

        return X

    @property
    def skip(self):
        return self._skip

    @property
    def bs(self):
        return self._bs


if __name__ == '__main__':
    img = cv2.imread('data/db/2.jpg')
    gt = cv2.imread('data/db/gt.2.png')
    #desc = {'blocksize': 8, 'skip': 1, 'kind': [['Hist', {'nbins': 16}]]}
    desc = {'blocksize': 8, 'skip': 2, 'kind': [['Hist', {'nbins': 16}], ['Gradient']]}

    feat = Features(desc)
    X, y = feat.run(img)

