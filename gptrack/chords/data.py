#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import cPickle as pickle
import gzip

from glob import glob
from hands import HandsDetector
from frameReader import FrameReader
from features import Features


class DumpFeatures():

    def __init__(self, dbroot, labels):
        assert os.path.exists(dbroot), '! dbroot...'
        self._gd = GetData(dbroot)
        self._feat = Features()
        self._labels = labels

    def run(self, outfile):
        X, y = self._gd.run(self._labels)
        X, y = self._feat.run(X), np.array(y)
        pickle.dump((X, y), gzip.open(outfile, 'wb'))


class GetData():

    def __init__(self, dbroot, prefix=['frame', 'mask', 'info']):
        assert os.path.exists(dbroot), '! dbroot...'
        self._dbroot = dbroot
        self._prefix = prefix

    def run(self, chords):
        X, y = [], []
        for key in chords.keys():
            print key
            data = [self.__my_glob(key, x) for x in self._prefix]
            for a, b, c in zip(data[0], data[1], data[2]):
                X.append([cv2.imread(a),
                          cv2.imread(b),
                          pickle.load(open(c, 'r'))])
            y += [chords[key] for n in range(len(data[0]))]
        return X, y

    def __my_glob(self, chord, pref):
        tmp = pref + '*' + chord + '*'
        files = glob(os.path.join(self._dbroot, tmp))
        files.sort()
        return files


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
    pass
