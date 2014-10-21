#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

from glob import glob
from features import Features, BlockHistogram, Pixel


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

    def __init__(self, path, labels, feat, discard=None, ext='.jpg',
                 prefix='gt.'):
        self._path = path
        self._ext = ext
        self._prefix = prefix
        self._c2l = Color2Label(labels, discard)
        self._feat = feat

    def run(self):
        assert os.path.exists(self._path), 'path...'
        query = '[!' + self._prefix + ']*' + self._ext

        X, y = np.array([]), np.array([])

        for fn in glob(os.path.join(self._path, query)):
            img, gt = self.__load_images(fn)
            gt = self._c2l.run(gt)
            tx, ty = self._feat.run(img, gt)

            X = np.vstack((X, tx)) if X.any() else tx
            y = np.hstack((y, ty)) if y.any() else ty

        return X, y

    def __load_images(self, fn):
        fngt = os.path.basename(fn).split(self._ext)[0]
        fngt = os.path.join(self._path, self._prefix + fngt + '.png')
        return cv2.imread(fn), cv2.imread(fngt)


if __name__ == '__main__':
    labels = {'0': [0, 0, 0], '1': [255, 0, 0], '2': [0, 0, 255]}
    feat = Features((BlockHistogram(16, 16), Pixel()), )

    dh = DataHandler('.', labels, feat)
    X, y = dh.run()

    db = DataBalancer()
    X, y = db.run(X, y)
