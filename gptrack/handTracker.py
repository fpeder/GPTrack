#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from frameReader import FrameReader
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

    def __init__(self, model='data/model/gopro.pkl', nframe=150,
                 display=False):
        self._hd = HandsDetector(model)
        self._nframe = nframe
        self._tracker = None
        self._vc = None
        self._display = display

    def run(self, vf):
        fr = FrameReader(vf)
        #assert os.path.exists(vf), '! video file...'
        #self._vc = cv2.VideoCapture(vf)
        state = State(self._nframe)
        strum = Strum()

        #while self._vc.isOpened():
        #    try:
        #        ret, frame = self._vc.read()
        #        assert frame.any()
        #    except AttributeError:
        #        break
        for frame in fr.next():

            frameg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if state.reinit():
                hands = self._hd.run(frame)
                pts = hands.get_points()
                self._tracker = PointTracker(frameg, pts)
            else:
                pts = self._tracker.run(frameg)

            strum.append(pts)
            state.update()

            if self._display:
                self.__show_points(frame, pts)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    hands.save('hands.pck')

        return strum

    def __show_points(self, frame, pts):
        frame = np.array(frame)
        for pt in pts:
            pt = pt.astype(np.int32)
            cv2.circle(frame, tuple(pt), 8, (255, 0, 0), -1)
        cv2.imshow('pts', frame)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    parser.add_argument("-o", "--outfile", type=str, help="output sequence")
    parser.add_argument("-d", "--display", action="store_true", help="display")

    args = parser.parse_args()

    ht = HandTracker(display=args.display)
    trj = ht.run(vf=args.infile)

    if args.outfile:
        trj.save(args.outfile)
