#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import GetData


if __name__ == '__main__':
    import argparse

    labels = {'Am0': 1, 'E0': 2, 'G0': 3, 'C0': 4,
              'Am7': 5, 'C7': 6, 'G7': 7, 'Bm7': 8}

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()

    gd = GetData(args.db, labels)
    gd.run(args.output)
