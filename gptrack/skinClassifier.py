#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import sys
import glob

import util

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.mixture import GMM


class SkinThresholder():

    def __init__(self, frame, mask, f=1.5):
        self._f = f
        self._th = self.__calc_thresh(frame, mask)

    def run(self, frame):
        if self._th:
            frame = util.rgb2ycrcb(frame)
            cr, cb = frame[:, :, 1], frame[:, :, 2]
            mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            mask[(cr >= self._th['cr'][0]) & (cr <= self._th['cr'][1]) &
                 (cb >= self._th['cb'][0]) & (cb <= self._th['cb'][1])] = 255
        skin = frame.copy()
        skin[mask == 0] = 0

        return skin, mask

    def __calc_thresh(self, frame, mask):
        frame = util.rgb2ycrcb(frame)[mask != 0]
        #frame = frame[mask != 0]

        cr, cb = frame[:, 1], frame[:, 2]
        pcr = [cr.mean(), np.sqrt(cr.var())]
        pcb = [cb.mean(), np.sqrt(cb.var())]

        f = self._f
        th = {'cr': [pcr[0] - f * pcr[1], pcr[0] + f * pcr[1]],
              'cb': [pcb[0] - f * pcb[1], pcb[0] + f * pcb[1]]}

        return th


class SkinQuickClassifier():

    def __init__(self, frame, mask, nc=1, th=0.85, ch=1):
        self._th = th
        self._ch = ch
        self._g = GMM(n_components=nc).fit(self.__reshape_data(frame, mask))

    def run(self, frame):
        if self._g:
            frame = util.rgb2ycrcb(frame)
            X = util.mat2vec(frame)
            X = X[:, self._ch:]

            prob = np.exp(self._g.score(X))
            prob = prob.reshape((frame.shape[0], frame.shape[1]))

            #mask = self.__threshold(prob)

            import pylab as plt
            import pdb; pdb.set_trace()

        return mask

    def __apply_mask(self, frame, mask):
        frame[mask == 0] = [0, 0, 0]

        return frame

    def __threshold(self, img):
        img[img > self._th] = 255
        img[img <= self._th] = 0

        return img

    def __reshape_data(self, frame, mask):
        frame = util.rgb2ycrcb(frame)
        skin = self.__apply_mask(frame, mask)

        X = util.mat2vec(skin)
        y = util.mat2vec(mask)

        nz = np.where(y != 0)[0]
        X = X[nz]
        X = X[:, self._ch:]

        return X


class SkinClassifier():

    def __init__(self, db='data/db/ibtd', ext='.jpg', max_depth=20):
        self._db, self._ext = db, ext
        self._X, self._y = None, None
        self._model = RandomForestClassifier(max_depth=max_depth)

    def train(self, nelem=-1, s=1):
        self.get_data(nelem, s)
        self.__balance_data()
        self._model.fit(self._X, self._y)

    def run(self, img):
        if self._model:
            sh = img.shape
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

            X = util.mat2vec(img)[:, 1:]
            p = self._model.predict(X)

            p = p.reshape((sh[0], sh[1]))
            p[p == 1] = 255

            skin = img
            skin[p == 0] = 0

            return skin, p

    def get_data(self, nelem=-1, s=1):
        if not os.path.exists(self._db):
            sys.stderr.write('error: ' + self._db + ' doesnt exist\n')
            sys.exit(-1)

        X, y = np.array([]), np.array([])
        imgfs = glob.glob(self._db + os.sep + '*' + self._ext)

        tot, count = len(imgfs), 0
        if tot == 0:
            sys.stderr.write('error: ' + self._db + ' is empty\n')
            sys.exit(-2)

        for imgf in imgfs:
            tmp = os.path.split(imgf)
            maskf = tmp[0] + '/Mask/' + tmp[1].split('.')[0] + '.bmp'

            if not X.any() and not y.any():
                X = util.load_as_features(imgf)[::s, 1:]
                y = util.load_as_labels(maskf)[::s]

            X = np.vstack((X, util.load_as_features(imgf)[::s, 1:]))
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


# class SkinThresholder():
#     R_CBCR = [[77, 127], [133, 173]]
#     R_H = (3, 43)

#     def __init__(self, flag='YCBCR'):
#         self._flag = flag

#     def run(self, img, th=None):
#         skin = np.zeros(img.shape, np.uint8)
#         mask = np.zeros(img.shape[:2], np.uint8)

#         if self._flag == 'HSV':
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#             h = img[:, :, 0]
#             mask[(h >= self.R_H[0]) & (h <= self.R_H[1])] = 255

#         elif self._flag == 'YCBCR':
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
#             cb, cr = img[:, :, 2], img[:, :, 1]

#             if not th:
#                 th = self.R_CBCR

#             mask[(cb > th[0][0]) & (cb < th[0][1]) &
#                  (cr > th[1][0]) & (cr < th[1][1])] = 255

#         else:
#             pass

#         skin = img.copy()
#         skin[mask == 0] = 0

#         return skin, mask

#     def set_thresholds(self, img, mask):
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
#         img[mask == 0] = 0

#         cb, cr = img[:, :, 2], img[:, :, 1]

#         th = []
#         for x in (cb, cr):
#             nz = x[x != 0]
#             mu, std = nz.mean(), np.sqrt(nz.var())
#             th.append([mu - 1.75*std, mu + 1.75*std])

#         return th


if __name__ == '__main__':
    sc = SkinClassifier()
    sc.train(100, 10)
    sc.save('data/model/forest.pkl')
