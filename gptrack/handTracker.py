#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from skin.classifier import SkinClassifier, SkinThresholder
from skin.enhancer import SkinEnhancer
from skin.filler import SkinFill

from hands.detector import PointDetector
from hands.tracker import PointTracker

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
        self._state = State()
        self._vc = None

    def run(self, vf, model='data/isabel.pkl'):
        self._vc = cv2.VideoCapture(vf)
        self._skin['classify'].load(model)
        trj = np.array([])

        while self._vc.isOpened():
            try:
                ret, frame = self._vc.read()
                frame = frame[::2, ::2, :]
            except TypeError:
                break

            #frameg = rgb2gray(frame)
            #st = self._state.get()

            skin, mask, pts = self.__detect_hands(frame, 'classify')

            # if st == self._state.REINIT:
            #     skin, mask, pts = self.__detect_hands(frame, 'classify')
            #     self._skin['threshold'] = SkinThresholder(frame, mask)
            #     self._points['track'] = PointTracker(frameg, pts)

            # elif st == self._state.REINIT_QUICK:
            #     skin, mask, pts = self.__detect_hands(frame, 'threshold')
            #     self._points['track'] = PointTracker(frameg, pts)

            # elif st == self._state.TRACK:
            #     pts = self._points['track'].run(frameg)

            #self._state.update()

            trj = self.__acc_points(trj, pts)

            self.__show_points(frame, pts)

            #self._points['track'].show()
            if cv2.waitKey(1) == ord('q'):
                break

        return trj

    def __detect_hands(self, frame, flag):
        skin, mask = self._skin[flag].run(frame)
        mask = self._skin['enhance'].run(mask)
        mask, pts = self._points['detect'].run(mask)
        return skin, mask, pts

    def __acc_points(self, trj, pts):
        if len(pts) == 2:
            pts = pts.reshape(1, 4)
            if pts[0, 0] > pts[0, 2]:
                pts[0, 0:2], pts[0, 2:4] = pts[0, 2:4], pts[0, 0:2]
        else:
            pts = np.array([-1, -1, -1, -1])
        trj = np.vstack((trj, pts)) if trj.any() else pts
        return trj

    def __show_points(self, frame, pts):
        frame = np.array(frame)
        for pt in pts.astype(np.int32):
            cv2.circle(frame, tuple(pt), 8, (255, 0, 0), -1)
        cv2.imshow('pts', frame)


if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    parser.add_argument("-o", "--outfile", type=str, help="output sequence")
    args = parser.parse_args()

    ht = HandTracker()
    trj = ht.run(vf=args.infile)

    if args.outfile:
        pickle.dump(trj, open(args.outfile, 'w'))
