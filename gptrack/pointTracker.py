#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from blobDetector import BlobDetector


class PointDetectorAndTracker():

    def __init__(self, tracker=cv2.calcOpticalFlowPyrLK,
                 detector=BlobDetector()):
        self._pts = np.array([])
        self._prev = np.array([])
        self._detector = detector
        self._tracker = tracker
        self._init = True

    def run(self, curr, init=None):
        if len(curr.shape) == 3 and curr.shape[2] == 3:
            curr = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        if init:
            self._init = init

        if self._init:
            self._pts = self._detector.run(curr)
            self._init = False

        elif self._prev.any() and self._pts.any():
            self._pts, a, b = self._tracker(self._prev, curr, self._pts)

        else:
            pass

        self._prev = curr

    def show(self, w='pts'):
        tmp = cv2.cvtColor(self._prev, cv2.COLOR_GRAY2BGR)
        if self._pts.any():
            for pt in self._pts:
                cv2.circle(tmp, tuple(pt), 12, (255, 0, 0), -1)

        cv2.imshow(w, tmp)


if __name__ == '__main__':
    pass
