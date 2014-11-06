#!/usr/bin/env python
# -*- coding: utf-8 -*-

from skin.classifier import SkinClassifier
from skin.data import DataHandler, DataConverter

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dbroot", type=str, required=True)
    parser.add_argument("-o", "--outfile", type=str, required=True)
    args = parser.parse_args()

    dh = DataHandler(args.dbroot, ['skin', 'body'], [1, 2])
    dh.run()
    dh.balance()
    X, y = dh.get()

    dc = DataConverter()
    X = dc.run(X)

    sc = SkinClassifier()
    sc.train(X, y, labels={'skin': 1, 'body': 2, 'bg': 0})
    sc.save(args.outfile)
