#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from skinClassifier import SkinClassifier, SkinThresholder
from skinFill import SkinFill
from pointTracker import PointDetectorAndTracker


class HandTracker():

    def __init__(self, sc=SkinClassifier(), pt=PointDetectorAndTracker(),
                 sf=SkinFill()):
        self._sc = sc
        self._pt = pt
        self._sf = sf
        self._st = SkinThresholder()
        self._vc = None

    def run(self, vf='../data/video/guitar.avi',
            model='../data/model/forest.pkl'):
        self._sc.load(model)
        self._vc = cv2.VideoCapture(vf)

        init = True
        count = 0
        th = None

        while self._vc.isOpened():
            ret, frame = self._vc.read()

            if init:
                skin, mask = self._sc.run(frame)
                th = self._st.set_thresholds(frame, mask)
                self._pt.run(mask, init)
                init = False
            else:
                skin, mask = self._st.run(frame, th)
                self._pt.run(mask)

            self._pt.show()

            if cv2.waitKey(1) == ord('q'):
                break

            count += 1
            if count == 50:
                init = True
                count = 0


if __name__ == '__main__':
    ht = HandTracker()
    ht.run()
