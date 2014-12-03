#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip
import cPickle as pickle

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


if __name__ == '__main__':
    import argparse

    argparse = argparse.ArgumentParser()
    argparse.add_argument('-i', '--indata', type=str, required=True)
    argparse.add_argument('-o', '--output', type=str, required=True)
    args = argparse.parse_args()

    assert os.path.exists(args.indata), '! in data...'
    X, y, labels = pickle.load(gzip.open(args.indata))

    cls = RandomForestClassifier(n_estimators=20)
    cls.fit(X, y)

    joblib.dump((cls, labels), args.output)
