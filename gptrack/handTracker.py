#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from skinClassifier import SkinClassifier, SkinQuickClassifier
from skinEnhancer import SkinEnhancer
from skinFill import SkinFill

from pointDetector import PointDetector
from pointTracker import PointTracker

from util import rgb2gray


class HandTracker():

    def __init__(self, sc=SkinClassifier(), st=SkinQuickClassifier,
                 sf=SkinFill(), se=SkinEnhancer(), pd=PointDetector(),
                 pt=PointTracker, count=50):
        self._skin = {'classify': sc, 'threshold': st, 'enhance': se,
                      'fill': sf}
        self._points = {'detect': pd, 'track': pt}
        self._count = count
        self._vc = None

    def run(self, vf, model='../data/model/forest.pkl'):
        self._skin['classify'].load(model)
        self._vc = cv2.VideoCapture(vf)

        init = True
        count = 0

        while self._vc.isOpened():
            ret, frame = self._vc.read()
            frameg = rgb2gray(frame)

            if init:
                skin, sking, mask = self._skin['classify'].run(frame)
                mask = self._skin['enhance'].run(mask)
                pts = self._points['detect'].run(mask)

                self._points['track'] = PointTracker(frameg, pts)

                #self._skin['threshold'] = SkinQuickClassifier(skin, hands)

                init = False

            else:
                #self._skin['threshold'].run(frame)
                pts = self._points['track'].run(frameg)

            self._points['track'].show()

            count += 1
            if count == self._count:
                count = 0
                init = True

            if cv2.waitKey(10) == ord('q'):
                break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    args = parser.parse_args()

    ht = HandTracker()
    ht.run(vf=args.infile)
