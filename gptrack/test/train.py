#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import SkinClassifier
from features import Features, BlockHistogram, Pixel

from sklearn.ensemble import RandomForestClassifier

if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-s', '--skip', type=int, default=1)
    parser.add_argument('-w', '--block', type=int, default=16)
    parser.add_argument('-n', '--nbins', type=int, default=16)
    args = parser.parse_args()

    path, w, n, s = args.db, args.block, args.nbins, args.skip
    output = args.output
    assert os.path.exists(path), '!path...'

    labels = {'0': [0, 0, 0], '1': [255, 0, 0], '2': [0, 0, 255]}
    feat = Features((BlockHistogram(w, w), Pixel()), s)
    model = RandomForestClassifier(min_samples_split=1, n_estimators=20)

    sc = SkinClassifier(model, labels, feat)
    sc.train(path, output=output)
