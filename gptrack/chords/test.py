#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import cPickle as pickle

from hands.detector import HandsDetector
from features import Features
from frameReader import FrameReader


class Test():

    def __init__(self, skin_model='data/model/gopro.pkl',
                 chords_model='data/model/chords.pkl'):

        assert os.path.exists(skin_model), '! skin model...'
        self._hd = HandsDetector(skin_model)

        assert os.path.exists(chords_model), '! chords model...'
        self._labels, self._model = pickle.load(open(chords_model, 'r'))

        self._feat = Features()

    def run(self, vf):
        fr = FrameReader(vf)
        for frame in fr.next():
            hands = self._hd.run(frame)
            cent, box = hands.left.cent, hands.left.box
            data = [[frame, None, (cent, box)]]
            x = self._feat.run(data)
            p = self._model.predict(x)[0]

            self.__show(frame, box, p)
            cv2.waitKey(5)

    def __show(self, frame, box, label):
        tmp = frame
        p, q = tuple(box[0]), tuple(box[1])
        cv2.rectangle(tmp, p, q, (255, 0, 0), 2)
        cv2.putText(tmp, self.__get_key(label), (p[0]+10, p[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3)
        cv2.imshow('chord', tmp)

    def __get_key(self, label):
        for name, x in self._labels.iteritems():
            if x == label:
                return name

if __name__ == '__main__':
    import argparse

    argparse = argparse.ArgumentParser()
    argparse.add_argument('-i', '--infile', type=str, required=True)
    args = argparse.parse_args()

    Test().run(args.infile)
