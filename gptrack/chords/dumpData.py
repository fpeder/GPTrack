#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import DumpData

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=str, required=True)
    parser.add_argument('-d', '--dstdir', type=str, required=True)
    parser.add_argument('-f', '--frames', nargs='+', type=int, required=True)
    args = parser.parse_args()

    gd = DumpData(args.dstdir)
    gd.run(args.infile, args.frames)
