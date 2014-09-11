#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from skinClassifier import SkinClassifier
from skinClassifier import SkinThresholder
from skinEnhancer import SkinEnhancer
from skinFill import SkinFill

from pointDetector import PointDetector
from pointTracker import PointTracker

from util import rgb2gray


class State():
    REINIT = 1
    REINIT_QUICK = 2
    TRACK = 3

    def __init__(self, init=True, quick=False, limit1=25, limit2=100):
        self._init = init
        self._quick = quick
        self._c1, self._c2 = 0, 0
        self._l1, self._l2 = limit1, limit2

    def get(self):
        if self._init and not self._quick:
            return self.REINIT

        if self._init and self._quick:
            return self.REINIT_QUICK

        if not self._init:
            return self.TRACK

    def update(self):
        self._c1 += 1
        self._c2 += 1

        self._init, self._quick = False, True

        if self._c1 > self._l1:
            self._init, self._c1 = True, 0
            self._quick = True

            if self._c2 > self._l2:
                self._quick, self._c2 = False, 0


class HandTracker():

    def __init__(self, sc=SkinClassifier(), st=SkinThresholder,
                 sf=SkinFill(), se=SkinEnhancer(), pd=PointDetector(),
                 pt=PointTracker):
        self._skin = {'classify': sc, 'threshold': None, 'enhance': se,
                      'fill': sf}
        self._points = {'detect': pd, 'track': pt}
        self._vc = None
        self._state = State()

    def run(self, vf, model='../data/model/forest_100_cbcr.pkl'):
        self._skin['classify'].load(model)
        self._vc = cv2.VideoCapture(vf)

        trj = np.array([])

        while self._vc.isOpened():
            ret, frame = self._vc.read()
            frameg = rgb2gray(frame)

            st = self._state.get()

            if st == self._state.REINIT:
                skin, mask, pts = self.__detect_hands(frame, 'classify')

                self._skin['threshold'] = SkinThresholder(frame, mask)
                self._points['track'] = PointTracker(frameg, pts)

            elif st == self._state.REINIT_QUICK:
                skin, mask, pts = self.__detect_hands(frame, 'threshold')
                self._points['track'] = PointTracker(frameg, pts)

            elif st == self._state.TRACK:
                pts = self._points['track'].run(frameg)

            self._state.update()

            if not trj.any():
                trj = pts[1]
            else:
                trj = np.vstack((trj, pts[1]))

            # ---- display -----
            self._points['track'].show()
            if cv2.waitKey(1) == ord('q'):
                break
        
        return trj

    def __detect_hands(self, frame, flag):
        skin, mask = self._skin[flag].run(frame)
        mask = self._skin['enhance'].run(mask)
        mask, pts = self._points['detect'].run(mask)

        return skin, mask, pts


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    args = parser.parse_args()

    ht = HandTracker()
    trj = ht.run(vf=args.infile)

    import pdb; pdb.set_trace()

    
