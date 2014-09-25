#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from util import rgb2ycrcb
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


class SkinClassifier():

    def __init__(self, model='RandomForestClassifier',
                 params='min_samples_split=1, n_estimators=20'):
        self._model = eval(model + '(' + params + ')')
        self._ready = False
        self._labels = None

    def train(self, X, y, labels=None):
        self._labels = labels
        self._model.fit(X, y)
        self._ready = True

    def run(self, img):
        if self._ready:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
            sh = img.shape
            X = img.reshape(sh[0] * sh[1], 3)
            pred = self._model.predict(X)
            pred = pred.reshape(sh[0], sh[1])

            return self.__get_skin(img, pred)

    def __get_skin(self, img, p):
        skin = img.copy()
        skin[p != self._labels['skin']] = 0
        mask = p.copy()
        mask[p == self._labels['skin']] = 255
        mask[mask != 255] = 0
        return skin, mask

    def save(self, fn):
        if self._ready:
            joblib.dump((self._model, self._labels), fn)

    def load(self, fn):
        self._model, self._labels = joblib.load(fn)
        self._ready = True


class SkinClassifierSoft():
    pass


class SkinThresholder():

    def __init__(self, frame, mask, f=1.5):
        self._f = f
        self._th = self.__calc_thresh(frame, mask)

    def run(self, frame):
        if self._th:
            frame = rgb2ycrcb(frame)
            cr, cb = frame[:, :, 1], frame[:, :, 2]
            mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            mask[(cr >= self._th['cr'][0]) & (cr <= self._th['cr'][1]) &
                 (cb >= self._th['cb'][0]) & (cb <= self._th['cb'][1])] = 255
        skin = frame.copy()
        skin[mask == 0] = 0
        return skin, mask

    def __calc_thresh(self, frame, mask):
        frame = rgb2ycrcb(frame)[mask != 0]
        cr, cb = frame[:, 1], frame[:, 2]
        pcr = [cr.mean(), np.sqrt(cr.var())]
        pcb = [cb.mean(), np.sqrt(cb.var())]

        f = self._f
        th = {'cr': [pcr[0] - f * pcr[1], pcr[0] + f * pcr[1]],
              'cb': [pcb[0] - f * pcb[1], pcb[0] + f * pcb[1]]}
        return th


if __name__ == '__main__':
    import pylab as plt

    sc = SkinClassifier()
    sc.load('data/isabel.pkl')

    img = cv2.imread('db/lam.mov.2.jpg')
    asd = sc.test(img)

    plt.imshow(asd)
    plt.show()
