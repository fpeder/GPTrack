#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle as pickle

from data import GetData
from features import Features
from sklearn.ensemble import RandomForestClassifier


class Train():

    def __init__(self, dbroot, labels={'Am': 1, 'E': 2, 'G': 3, 'C': 4}):
        assert os.path.exists(dbroot), '! dbroot...'
        self._gd = GetData(dbroot)
        self._feat = Features()
        self._labels = labels

    def run(self, outfile):
        X, y = self._gd.run(self._labels)
        X = self._feat.run(X)

        pickle.dump((X, y), open('data.pck', 'w'))

        model = RandomForestClassifier(n_estimators=20)
        model.fit(X, y)

        pickle.dump((self._labels, model), open(outfile, 'w'))


if __name__ == '__main__':
    import argparse

    argparse = argparse.ArgumentParser()
    argparse.add_argument('-d', '--dbroot', type=str, required=True)
    argparse.add_argument('-o', '--output', type=str, required=True)
    args = argparse.parse_args()

    Train(args.dbroot).run(args.output)
