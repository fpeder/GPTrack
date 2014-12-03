#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import cPickle as pickle

from sklearn.externals import joblib

from hands.detector import HandsDetector
from features import Chord2Vec
from frameReader import FrameReader


class ChordDetector():

    def __init__(self, cmod):
        assert os.path.exists(cmod), '! chord model'
        self._cls, labels = joblib.load(cmod)
        self._feat = Chord2Vec()
        self._labels = {v: k for k, v in labels.items()}

    def run(self, img, hand):
        x = self._feat.run(img, hand.mask, hand.box)
        p = self._cls.predict(x)
        return self._labels[int(p)]


class Test():

    def __init__(self, cmod='data/model/chords.pkl',
                 smod='data/model/gopro.pkl'):
        self._hd = HandsDetector(smod)
        self._cd = ChordDetector(cmod)

    def run(self, vf):
        fr = FrameReader(vf)
        for frame in fr.next():
            hands = self._hd.run(frame)
            frameg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ch = self._cd.run(frameg, hands.left)
            
            self.__show(frame, hands.left.box, ch)
            cv2.waitKey(4)

    def __show(self, frame, box, label):
        tmp = frame
        p, q = tuple(box[0]), tuple(box[1])
        cv2.rectangle(tmp, p, q, (255, 0, 0), 2)
        cv2.putText(tmp, label, (p[0]+10, p[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3)
        cv2.imshow('chord', tmp)


if __name__ == '__main__':
    import argparse

    argparse = argparse.ArgumentParser()
    argparse.add_argument('-i', '--infile', type=str, required=True)
    args = argparse.parse_args()

    test = Test()
    test.run(args.infile)
