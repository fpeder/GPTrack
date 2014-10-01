#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from hands.detector import HandsDetector
from hands.tracker import PointTracker
from strum.strum import Strum


class State():

    def __init__(self, nframe=50):
        self._init = True
        self._nframe = nframe
        self._count = 0

    def reinit(self):
        return self._init

    def update(self):
        self._count += 1
        if self._count > self._nframe:
            self._init = True
            self._count = 0
        else:
            self._init = False
            self._count += 1


class HandTracker():

    def __init__(self, model='data/model/gopro.pkl'):
        self._hd = HandsDetector(model)
        self._tracker = None
        self._vc = None

    def run(self, vf):
        self._vc = cv2.VideoCapture(vf)
        state = State(350)
        strum = Strum()

        while self._vc.isOpened():
            try:
                ret, frame = self._vc.read()
                frameg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except TypeError:
                break

            if state.reinit():
                hands = self._hd.run(frame)
                pts = hands.get_points()
                self._tracker = PointTracker(frameg, pts)
            else:
                pts = self._tracker.run(frameg)

            strum.append(pts)
            state.update()

            self.__show_points(frame, pts)
            if cv2.waitKey(1) == ord('q'):
                break

        return strum

    def __show_points(self, frame, pts):
        frame = np.array(frame)
        for pt in pts:
            pt = pt.astype(np.int32)
            cv2.circle(frame, tuple(pt), 8, (255, 0, 0), -1)
        cv2.imshow('pts', frame)


# class State():
#     REINIT = 1
#     REINIT_QUICK = 2
#     TRACK = 3

#     def __init__(self, init=True, quick=False, limit1=25, limit2=100):
#         self._init = init
#         self._quick = quick
#         self._c1, self._c2 = 0, 0
#         self._l1, self._l2 = limit1, limit2

#     def get(self):
#         if self._init and not self._quick:
#             return self.REINIT
#         if self._init and self._quick:
#             return self.REINIT_QUICK
#         if not self._init:
#             return self.TRACK

#     def update(self):
#         self._c1 += 1
#         self._c2 += 1
#         self._init, self._quick = False, True
#         if self._c1 > self._l1:
#             self._init, self._c1 = True, 0
#             self._quick = True
#             if self._c2 > self._l2:
#                 self._quick, self._c2 = False, 0


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
