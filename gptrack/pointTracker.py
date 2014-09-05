#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class PointTracker():

    def __init__(self, tracker=cv2.calcOpticalFlowPyrLK):
        self._tracker = tracker
        self._prev = np.array([])
        self._pts = np.array([])

    def init(self, curr, pts):
        self._prev = curr
        self._pts = pts

    def run(self, curr):
        if self._prev.any() and self._pts.any():
            pts = self._pts.astype(np.float32)
            self._pts, a, b = self._tracker(self._prev, curr, pts)

        self._prev = curr

        return self._pts

    def show(self, w='pts'):
        if not len(self._prev.shape) == 3:
            tmp = cv2.cvtColor(self._prev, cv2.COLOR_GRAY2BGR)

        for pt in self._pts.astype(np.int32):
            cv2.circle(tmp, tuple(pt), 12, (255, 0, 0), -1)

        cv2.imshow(w, tmp)


if __name__ == '__main__':
    pass
