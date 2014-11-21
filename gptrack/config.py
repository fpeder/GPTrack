#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

from glob import glob


class Config():

    def __init__(self, conf={}):
        self._config = conf

    def load(self, fn):
        assert os.path.exists(fn), '!fn...'
        yml = yaml.load(open(fn, 'r'))

        model, featspec, labels, trainspec = self.__parse(yml)

        self._config['model'] = ModelConfig(model, featspec)
        self._config['data'] = DataConfig(labels, trainspec)
        self._config['db'] = DbConfig(trainspec['dbroot'])

    def __parse(self, conf):
        model = conf['model']
        trainspec = conf['trainspec']
        featspec = conf['features']
        labels = {}
        for lab in conf['labels']:
            labels[str(lab['id'])] = lab['color']
        return model, featspec, labels, trainspec

    @property
    def get(self):
        return self._config

    @property
    def data(self):
        return self._config['data']

    @property
    def db(self):
        return self._config['db']

    @property
    def model(self):
        return self._config['model']


class ModelConfig():

    def __init__(self, cls, features):
        self._cls = cls
        self._features = features

    @property
    def cls(self):
        return self._cls

    @property
    def features(self):
        return self._features


class DataConfig():

    def __init__(self, labels, trainspec):
        self._labels = labels
        self._ds = trainspec['downsample']
        self._discard = eval(trainspec['discard'])
        self._balance = eval(trainspec['balance'])

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
        gtr.sort()
        img = [x for x in files if not test(x)]
        img.sort()
        return zip(img, gtr)


if __name__ == '__main__':
    caz = DbConfig('db')
    caz.glob()
