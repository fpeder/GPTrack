#!/usr/bin/env python
# -*- coding: utf-8 -*-

from skinClassifier import SkinClassifier

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="traning database")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="output model")
    args = parser.parse_args()

    sc = SkinClassifier(db=args.input)
    sc.train(100)
    sc.save(args.output)
