#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from data import DataHandler, DataBalancer
from util import makeCallableString

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from os.path import exists


class SkinClassifier():

    def __init__(self):
        self._cls = None
        self._dh = None

    def train(self, config):
        self._cls = self.__parse(config.model.cls)
        self._dh = DataHandler(config.data, config.db, config.model.features)
        X, y = self._dh.run()
        if config.data.balance:
            X, y = DataBalancer().run(X, y)
        self._cls.fit(X, y)

    def run(self, img):
        M, N = img.shape[:-1]
        X = self._dh.get_features(img)
        y = self._cls.predict(X)
        y = self._dh.reshape(y, M, N)
        return self.__get_skin(img, y)

    def __get_skin(self, img, p):
        skin = img.copy()
        skin[p != 1] = 0
        mask = p.copy()
        mask = mask.astype(np.uint8)
        mask[p == 1] = 255
        mask[mask != 255] = 0
        return skin, mask

    def save(self, fn):
        joblib.dump((self._cls, self._dh), fn)

    def load(self, fn):
        assert exists, '!fn...'
        self._cls, self._dh = joblib.load(fn)

    def __parse(self, desc):
        tmp = makeCallableString(desc)
        return eval(tmp)


if __name__ == '__main__':
    import cv2
    import sys
    import pylab as plt

    img = cv2.imread(sys.argv[1])
    assert img.any(), '!img...'

    sc = SkinClassifier()
    sc.load('model/asd.pkl')
    y = sc.run(img)

    plt.imshow(y)
    plt.show()
