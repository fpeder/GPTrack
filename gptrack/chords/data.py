#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip
import cv2
import cPickle as pickle
import numpy as np

from glob import glob
from progress.bar import Bar
from features import Chord2Vec


class Loader():

    def __init__(self, dbroot, labels):
        assert os.path.exists(dbroot), '! dbroot...'
        self._dbroot = dbroot
        self._labels = labels

    def next(self):
        for key in self._labels.keys():
            ch, lab = key, self._labels[key]
            frame, mask, info = (self.__my_glob(ch, 'frame'),
                                 self.__my_glob(ch, 'mask'),
                                 self.__my_glob(ch, 'info'))
            for f, m, i in zip(frame, mask, info):
                a = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)
                b = cv2.imread(m)
                c = pickle.load(open(i, 'r'))
                yield lab, a, b, c[1]

    def __my_glob(self, ch, pref):
        tmp = pref + '*' + ch + '*'
        files = glob(os.path.join(self._dbroot, tmp))
        files.sort()
        return files


class GetData():

    def __init__(self, dbroot, labels, count=10):
        self._loader = Loader(dbroot, labels)
        self._feat = Chord2Vec()
        self._count = count
        self._labels = labels
        self._N = len(os.path.join(dbroot, '*.jpg'))

    def run(self, output):
        X, y = [], []
        bar = Bar('Processing', max=self._N)
        for lab, frame, mask, box in self._loader.next():
            X.append(self._feat.run(frame, mask, box))
            y.append(lab)
            bar.next()
        bar.finish()

        if output:
            X, y = np.array(X), np.array(y)
            
            pickle.dump((X, y, inv_lab), gzip.open(output, 'wb'))
        else:
            return X, y


if __name__ == '__main__':
    pass
