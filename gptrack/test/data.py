#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from features import Features
from config import DataConfig, DbConfig


def split(img):
    return [img[:, :, 0], img[:, :, 1], img[:, :, 2]]


class Color2Label():

    def __init__(self, labels, discard=None):
        self._labels = labels
        self._discard = discard

    def run(self, img):
        img = self.__discard(img)
        gt = np.zeros(img.shape[:-1], np.uint8)
        b, g, r = split(img)
        for lab, col in self._labels.iteritems():
            gt[self.__find_color(r, g, b, col)] = int(lab)
        return gt

    def __discard(self, img):
        if self._discard:
            col = self._labels.pop(self._discard)
            b, g, r = split(img)
            img[self.__find_color(r, g, b, col)] = 0
        return img

    def __find_color(self, r, g, b, col):
        return (r == col[0]) & (g == col[1]) & (b == col[2])


class DataBalancer():

    def __init__(self):
        pass

    def run(self, X, y):
        num, lab, tofix = self.__to_fix(y)
        newX = X[y == lab]
        newy = y[y == lab]
        for l in tofix:
            tmpX = X[y == l]
            np.random.shuffle(tmpX)
            newX = np.vstack((newX, tmpX[0:num, :]))
            newy = np.hstack((newy, l*np.ones(num, np.uint8)))
        return newX, newy

    def __to_fix(self, y):
        tofix = {}
        for lab in np.unique(y):
            tofix[str(lab)] = len(y[y == lab])
        lab = min(tofix, key=tofix.get)
        num = tofix.pop(lab)
        return num, int(lab), [int(x) for x in tofix.keys()]


class DataHandler():

    def __init__(self, dataconf, dbconf, featdesc):
        self._config = {'data': dataconf, 'db': dbconf}
        self._c2l = Color2Label(dataconf.labels, dataconf.discard)
        self._features = Features(featdesc)

    def run(self):
        X = np.array([])
        y = np.array([])
        for im, gt in self._config['db'].glob():
            im, gt = self.__load_data(im, gt)
            tx, ty = self._features.run(im, gt)
            X = np.vstack((X, tx)) if X.any() else tx
            y = np.hstack((y, ty)) if y.any() else ty
        return X, y

    def get_features(self, img):
        X, _ = self._features.run(img)
        return X

    def reshape(self, y, M, N):
        s = self._features.skip
        w = self._features.bs
        Ms, Ns = np.ceil((M-w)/s), np.ceil((N-w)/s)
        y = y.reshape(Ms, Ns)
        y = np.kron(y, np.ones((s, s), np.int32))
        return y

    def __load_data(self, img, gt):
        im = cv2.imread(img)
        gt = cv2.imread(gt)
        ds = self._config['data'].ds
        if ds:
            im = im[::ds, ::ds]
            gt = gt[::ds, ::ds]
        gt = self._c2l.run(gt)
        return im, gt


if __name__ == '__main__':
    dh = DataHandler(dataconf, dbconf, featdesc)
    X, y = dh.run()

    import pdb; pdb.set_trace()
