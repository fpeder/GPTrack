#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import cPickle as pickle

from hands import HandsDetector
from frameReader import FrameReader


class DumpData():

    def __init__(self, dst, model='data/model/gopro.pkl'):
        assert os.path.exists(dst), '! dst...'
        self._hd = HandsDetector(model)
        self._dst = dst
        self._vc = None

    def run(self, vf, nframes):
        self._vf = vf
        fr = FrameReader(vf)
        n, c = nframes.pop(0), 0
        for frame in fr.next():
            c += 1
            if c == n:
                n = nframes.pop(0)
                hands = self._hd.run(frame)
                self.__dump(frame, hands.left, n)
                if not nframes:
                    break

    def __dump(self, frame, hand, n):
        fn = os.path.basename(self._vf)
        base = fn.split('.')[0] + '.' + str(n)
        pt = os.path.join(self._dst, 'frame.' + base + '.jpg')
        cv2.imwrite(pt, frame)
        pt = os.path.join(self._dst, 'mask.' + base + '.jpg')
        cv2.imwrite(pt, hand.mask)
        pt = os.path.join(self._dst, 'info.' + base + '.pck')
        pickle.dump((hand.cent, hand.box), open(pt, 'w'))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=str, required=True)
    parser.add_argument('-d', '--dstdir', type=str, required=True)
    parser.add_argument('-f', '--frames', nargs='+', type=int, required=True)
    args = parser.parse_args()

    gd = DumpData(args.dstdir)
    gd.run(args.infile, args.frames)
