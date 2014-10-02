#!/usr/bin/env python
# -*- coding: utf-8 -*-

from strum import Strum
from strum import UpDown

if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True)
    parser.add_argument("-o", "--outfile", type=str, required=True)
    args = parser.parse_args()

    s = Strum()
    s.load(args.infile)

    pts = s.right
    ud = UpDown()
    asd = ud.run(pts)

    pickle.dump(asd, open(args.outfile, 'w'))
