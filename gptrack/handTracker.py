#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from skinClassifier import SkinClassifier
from skinFill import SkinFill
from pointTracker import PointDetectorAndTracker


class HandTracker():

    def __init__(self, sc=SkinClassifier(), pt=PointDetectorAndTracker(),
                 sf=SkinFill()):
        self._sc = sc
        self._pt = pt
        self._sf = sf
        self._vc = None

    def run(self, vf='../data/video/guitar.avi',
            model='../data/model/forest.pkl'):
        self._sc.load(model)
        self._vc = cv2.VideoCapture(vf)

        while self._vc.isOpened():
            ret, frame = self._vc.read()

            skin, mask = self._sc.run(frame)
            self._pt.run(mask)
            self._pt.show()

            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == '__main__':
    ht = HandTracker()
    ht.run()
