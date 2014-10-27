#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Hist():

    def __init__(self, nbins, rangee=(0, 255)):
        self._nbins = nbins
        self._range = rangee
        self._length = self._nbins * 3

    def run(self, img):
        h = [np.histogram(img[:, :, i], self._nbins, self._range)[0] for i in
             range(img.shape[2])]
        h = np.array(h).reshape(-1)
        return h

    @property
    def length(self):
        return self._length


class Features():

    def __init__(self, desc):
        self._feat = self.__set(desc)

    def run(self, img, gt=np.array([])):
        X = [self.__to_vectors(x.run(img)) for x in self._feat]
        X = np.hstack((X))
        gt = gt.reshape(-1) if gt.any() else gt
        return X, gt

    def __set(self, desc):
        return [x[0](x[1], x[2]) for x in desc]

    def __to_vectors(self, x):
        M, N, L = x.shape
        return x.reshape(M * N, L)


if __name__ == '__main__':
    from blockproc import BlockProcess

    img = cv2.imread('2.jpg')
    gt = cv2.imread('gt.2.png')

    kind = BlockProcess(8, Hist(16))
    feat = Features([kind])
    X, y = feat.run(img, gt)

    import pdb; pdb.set_trace()
