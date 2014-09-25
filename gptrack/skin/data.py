#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

from glob import glob


class DataConverter():

    def __init__(self, transf=cv2.COLOR_BGR2YCR_CB, nfeat=2):
        self._transf = transf
        self._nfeat = nfeat

    def run(self, X):
        X = X.reshape((X.shape[0], 1, X.shape[1]))
        X = cv2.cvtColor(X, self._transf)
        X = X.reshape(X.shape[0], X.shape[2])
        return X


class PartsHandler():

    def __init__(self, root, prefix, labels, zero=0):
        self._root = root
        self._prefix = prefix
        self._labels = labels
        self._zero = zero
        self._X, self._y = np.array([]), np.array([])
        self._acc = np.array([])

    def run(self, img, fn):
        assert os.path.exists(self._root)
        for parts, label in zip(self._prefix, self._labels):
            bn = os.path.basename(fn)
            part_file = os.path.join(self._root, parts + '.' + bn)
            part = cv2.imread(part_file)
            self.__append_data(part, label)

        self.__append_background_data(img)
        return self._X, self._y

    def __append_data(self, img, label):
        assert img.any()
        tx = self.__non_zero(img)
        ty = label * np.ones(tx.shape[0], np.uint8)

        if self._X.any() or self._y.any():
            self._X = np.vstack((self._X, tx))
            self._y = np.hstack((self._y, ty))
            self._acc += img
        else:
            self._X = tx
            self._y = ty
            self._acc = img

    def __append_background_data(self, img):
        assert self._acc.any()
        tx = img[(self._acc[:, :, 0] == self._zero) &
                 (self._acc[:, :, 1] == self._zero) &
                 (self._acc[:, :, 2] == self._zero)]
        ty = np.zeros(tx.shape[0], np.uint8)
        self._X = np.vstack((self._X, tx))
        self._y = np.hstack((self._y, ty))

    def __non_zero(self, img):
        nz = img[(img[:, :, 0] != self._zero) &
                 (img[:, :, 1] != self._zero) &
                 (img[:, :, 2] != self._zero)]
        return nz


class DataHandler():

    def __init__(self, dbroot, prefix, labels, mask='mask', ext='.jpg',
                 zero=0):
        self._dbroot, self._ext = dbroot, ext
        self._ph = PartsHandler(os.path.join(dbroot, mask), prefix, labels,
                                zero)
        self._labels = labels
        self._X = np.array([])
        self._y = np.array([])

    def run(self):
        assert os.path.exists(self._dbroot)
        for fn in glob(os.path.join(self._dbroot, '*' + self._ext)):
            assert os.path.exists(fn)
            img = cv2.imread(fn)
            X, y = self._ph.run(img, fn)
            self.__append_data(X, y)

    def balance(self):
        assert self._X.any() and self._y.any()
        X, y = self._X, self._y
        labels, num = self.__sort_labels()

        idx = np.where(y == labels[0])[0]
        tX = X[idx, :]
        ty = labels[0] * np.ones(num, np.uint8)
        for lab in labels[1:]:
            idx = np.where(y == lab)[0]
            tmp = X[idx, :]
            np.random.shuffle(tmp)
            tX = np.vstack((tX, tmp[1:num+1, :]))
            ty = np.hstack((ty, lab * np.ones(num, np.uint8)))

        self._X, self._y = tX, ty

    def sub_sample_data(self, s):
        self._X = self._X[1:s:, :]
        self._y = self._y[1:s:]

    def get(self):
        return self._X, self._y

    def __sort_labels(self):
        labels = self._labels
        labels.append(0)
        nelem = np.array([len(self._y[self._y == x]) for x in labels])
        num = nelem.min()
        labels = np.array(labels)
        labels = labels[np.argsort(nelem)]
        return labels, num

    def __append_data(self, X, y):
        if self._X.any() and self._y.any():
            self._X = np.vstack((self._X, X))
            self._y = np.hstack((self._y, y))
        else:
            self._X = X
            self._y = y


if __name__ == '__main__':
    dh = DataHandler('../db', ['skin', 'body'], [1, 2])
    dh.run()
    dh.balance()
    (X, y) = dh.get()

    dc = DataConverter()
    X = dc.run(X)

    import pdb; pdb.set_trace()

