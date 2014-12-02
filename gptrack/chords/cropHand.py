#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import cPickle as pickle
import numpy as np

SIZE = (64, 64)


class Crop():

    def __init__(self, size):
        self._sz = size

    def run(self, imgs, box):
        return [self.__crop(x, box) for x in imgs]

    def __crop(self, x, box):
        p, q = box[0], box[1]
        x = x[p[1]:q[1], p[0]:q[0]]
        return x


class CropHand():

    def __init__(self, th=1.5, niter=5, sz=7,
                 strel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))):
        self._strel = strel
        self._niter = niter
        self._th = th
        self._sz = sz
        self._crop = Crop(SIZE)

    def run(self, img, mask, box):
        img, mask = self._crop.run([img, mask], box)

        mask1, mask2 = self.__prep(mask)

        pt, r = self.__min_cirlce(mask2)
        dist = self.__dist(mask1 + mask2, pt, r)

        mask1[dist >= self._th] = 0

        box = self.__new_box(mask1)
        img = self._crop.run([img], box)[0]
        return cv2.resize(img, SIZE)

    def __new_box(self, mask):
        x, y = np.where(mask == 1)
        p = [x.min(), y.min()]
        q = [x.max(), y.max()]
        return p, q

    def __dist(self, x, q, r):
        y = np.zeros(x.shape, np.float32)
        i, j = np.where(x == 1)
        for i, j in zip(i, j):
            p = np.array([i, j])
            y[i, j] = np.linalg.norm(p - q, 2) / r
        return y

    def __prep(self, mask):
        mask1 = mask[:, :, 0]
        mask1 = cv2.medianBlur(mask1, self._sz)
        mask1[mask1 >= 1] = 1
        mask2 = cv2.erode(mask1, self._strel, iterations=self._niter)
        return mask1, mask2

    def __min_cirlce(self, img):
        tmp = img.copy()
        cnt, _ = cv2.findContours(tmp, cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_NONE)
        L = [len(x) for x in cnt]
        pts = cnt[L.index(max(L))]
        (y, x), r = cv2.minEnclosingCircle(pts)
        pt = [int(x), int(y)]
        return pt, r


if __name__ == '__main__':
    import sys

    n = sys.argv[1]
    img = cv2.imread('frame'+n+'.jpg')
    mask = cv2.imread('mask'+n+'.jpg')
    info = pickle.load(open('info'+n+'.pck', 'r'))
    box = info[1]

    lh = CropHand()
    lh.run(img, mask, box)
