#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import os
import util

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


class SkinThresholder():
    R_CB = (77, 127)
    R_CR = (133, 173)
    R_H = (3, 43)

    def __init__(self, flag='YCBCR'):
        self._flag = flag

    def run(self, img):
        skin = np.zeros(img.shape, np.uint8)
        mask = np.zeros(img.shape[:2], np.uint8)

        if self._flag == 'HSV':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h = img[:, :, 0]
            mask[(h >= self.R_H[0]) & (h <= self.R_H[1])] = 255

        elif self._flag == 'YCBCR':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
            cb, cr = img[:, :, 2], img[:, :, 1]
            mask[(cb >= self.R_CB[0]) & (cb <= self.R_CB[1]) &
                 (cr >= self.R_CR[0]) & (cr <= self.R_CR[1])] = 255

        else:
            pass

        skin = img.copy()
        skin[mask == 0] = 0

        return skin, mask


class SkinClassifier():

    def __init__(self, db='data/db/ibtd', ext='.jpg'):
        self._db, self._ext = db, ext
        self._X, self._y = None, None
        self._model = RandomForestClassifier(max_depth=20)

    def train(self, nelem=-1, s=1):
        self.get_data(nelem, s)
        self.__balance_data()
        self._model.fit(self._X, self._y)

    def run(self, img):
        if self._model:
            imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
            sh = img.shape

            p = self._model.predict(util.mat2vec(img))
            p = p.reshape((sh[0], sh[1]))

            skin = imgg
            skin[p == 0] = 0
            p[p == 1] = 255

            return (skin, p)

    def get_data(self, nelem=-1, s=1):
        X = np.array([])
        y = np.array([])

        imgfs = glob.glob(self._db + os.sep + '*' + self._ext)
        tot = len(imgfs)
        count = 0

        for imgf in imgfs:
            tmp = os.path.split(imgf)
            maskf = tmp[0] + '/Mask/' + tmp[1].split('.')[0] + '.bmp'

            if not X.any() and not y.any():
                X = util.load_as_features(imgf)[::s, :]
                y = util.load_as_labels(maskf)[::s]

            X = np.vstack((X, util.load_as_features(imgf)[::s, :]))
            y = np.hstack((y, util.load_as_labels(maskf)[::s]))

            count += 1
            print str(count) + '/' + str(tot)

            if nelem == -1:
                continue
            if count == nelem:
                break

        self._X = X
        self._y = y

        return (X, y)

    def __balance_data(self):
        idx = np.argsort(self._y)
        np.random.shuffle(idx[self._y == 0])

        l0 = len(self._y[self._y == 0])
        l1 = len(self._y[self._y == 1])
        idx = np.hstack((idx[0:l1], idx[l0:-1]))

        self._X = self._X[idx, :]
        self._y = self._y[idx]

    def save(self, fn):
        joblib.dump(self._model, fn)

    def load(self, fn):
        if not self._model:
            self._model = joblib.load(fn)

    @property
    def model(self):
        return self._model

    @property
    def data(self):
        return (self._X, self._y)


if __name__ == '__main__':
    sc = SkinClassifier()
    sc.train(100, 10)
    sc.save('data/model/forest.pkl')
