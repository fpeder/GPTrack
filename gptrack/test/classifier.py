#!/usr/bin/env python
# -*- coding: utf-8 -*-


from data import DataHandler, DataBalancer

from sklearn.externals import joblib


class SkinClassifier():

    def __init__(self, model, labels, features, discard=None, balance=True):
        self._model = model
        self._labels = labels
        self._discard = discard
        self._features = features
        self._balance = balance

    def predicit(self, img):
        X, _ = self._features.run(img)
        pass

    def train(self, path, ext='.jpg,', prefix='gt.', output=None):
        dh = DataHandler(path, self._labels, self._features)
        X, y = dh.run()
        if self._balance:
            db = DataBalancer()
            X, y = db.run(X, y)

        self._model.fit(X, y)
        if output:
            joblib.dump((self._model, self._labels), output)

    def load(self, fn):
        self._model, self._labels = joblib.load(fn)
