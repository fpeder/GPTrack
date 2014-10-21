#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Pixel():

    def __init__(self):
        self.img = np.array([])

    def run(self, i, j):
        assert self.img.any(), '!img...'
        return self.img[i, j, :]


class BlockHistogram():

    def __init__(self, w=16, bins=16, r=(0, 255)):
        self.img = np.array([])
        self._w = w
        self._bins = bins
        self._r = r

    def run(self, i, j):
        assert self.img.any(), 'img'
        tmp = self.__get_block(i, j)
        hist = [np.histogram(tmp[:, :, ch], self._bins, self._r)[0] for
                ch in range(3)]
        hist = np.array([hist]).reshape(-1)
        return hist

    def __get_block(self, i, j):
        N = self.img.shape[1]
        M = self.img.shape[0]
        si = i - self._w/2 if i - self._w/2 >= 0 else 0
        ei = i + self._w/2 if i + self._w/2 < M else M
        sj = j - self._w/2 if j - self._w/2 >= 0 else 0
        ej = j + self._w/2 if j + self._w/2 < N else N
        return self.img[si:ei, sj:ej]


class Features():

    def __init__(self, features, step=4):
        self._asd = features
        self._step = step

    def run(self, img, gt=np.array([])):
        X, y = np.array([]), np.array([])

        for i in range(len(self._asd)):
            self._asd[i].img = img

        for i in range(0, img.shape[0], self._step):
            for j in range(0, img.shape[1], self._step):
                tx = [x.run(i, j) for x in self._asd]
                tx = np.hstack((tx[0], tx[1]))

                X = np.vstack((X, tx)) if X.any() else tx
                if gt.any():
                    y = np.hstack((y, gt[i, j])) if y.any() else gt[i, j]

        return X, y


if __name__ == '__main__':
    img = cv2.imread('2.jpg')
    gt = cv2.imread('gt.2.png')

    #feat = Features((Pixel(img), BlockHistogram(img, 16, 16)), 4)
    #X, y = feat.run(img, gt)
    #import pdb; pdb.set_trace()
