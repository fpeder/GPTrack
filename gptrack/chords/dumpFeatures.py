#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import DumpFeatures

lab = {'Am0': 1, 'E0': 2, 'G0': 3, 'C0': 4,
       'Am7': 5, 'Bm7': 6, 'C7': 7, 'G7': 8}

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', type=str, required=True)
    parser.add_argument('-o', '--outfile', type=str, required=True)
    arg = parser.parse_args()

    df = DumpFeatures(arg.db, lab)
    df.run(arg.outfile)
