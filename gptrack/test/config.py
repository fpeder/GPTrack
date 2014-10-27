#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from glob import glob


class ModelConfig():

    def __init__(self, model, features):
        self._model = model
        self._features = features

    @property
    def model(self):
        return self._model

    @property
    def features(self):
        return self._features


class DataConfig():

    def __init__(self, labels, ds=None, discard=None, balance=True):
        self._labels = labels
        self._ds = ds
        self._discard = discard
        self._balance = balance

    @property
    def labels(self):
        return self._labels

    @property
    def ds(self):
        return self._ds

    @property
    def discard(self):
        return self._discard

    @property
    def balance(self):
        return self._balance


class DbConfig():

    def __init__(self, path, ext='.jpg', prefix='gt.'):
        self._path = path
        self._ext = ext
        self._prefix = prefix

    def glob(self):
        assert os.path.exists(self._path), '!path...'
        files = glob(os.path.join(self._path, '*'))

        def test(x):
            return os.path.basename(x).startswith(self._prefix)

        gtr = [x for x in files if test(x)]
        img = [x for x in files if not test(x)]
        return zip(img, gtr)


        
if __name__ == '__main__':
    caz = DbConfig('db')
    caz.glob()
