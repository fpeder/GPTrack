#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from skinClassifier import SkinClassifier, SkinThresholder
from skinEnhancer import SkinEnhancer
from skinFill import SkinFill

from pointDetector import PointDetector
from pointTracker import PointTracker


class HandTracker():

    def __init__(self, sc=SkinClassifier(), st=SkinThresholder(),
                 sf=SkinFill(), se=SkinEnhancer(), pd=PointDetector(),
                 pt=PointTracker()):

        self._skin = {'classify': sc, 'threshold': st, 'enhance': se,
                      'fill': sf}
        self._points = {'detect': pd, 'track': pt}
        self._vc = None

    def run(self, vf, model='../data/model/forest.pkl'):
        self._skin['classify'].load(model)
        self._vc = cv2.VideoCapture(vf)

        init = True
        count = 0

        while self._vc.isOpened():
            ret, frame = self._vc.read()

            sking, mask = self._skin['classify'].run(frame)
            mask = self._skin['enhance'].run(mask)

            if init:
                pts = self._points['detect'].run(mask)
                self._points['track'].init(sking, pts)
                init = False

            else:
                pts = self._points['track'].run(sking)

            self._points['track'].show()

            count += 1

            if cv2.waitKey(1) == ord('q'):
                break



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    args = parser.parse_args()

    ht = HandTracker()
    ht.run(vf=args.infile)
