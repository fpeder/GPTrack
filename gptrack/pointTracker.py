#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from util import gray2rgb


class PointTracker():

    def __init__(self, prev, pts, tracker=cv2.calcOpticalFlowPyrLK):
        self._prev = prev
        self._pts = pts
        self._tracker = tracker

    def run(self, curr):
        if self._prev.any() and self._pts.any():
            pts = self._pts.astype(np.float32)
            self._pts, a, b = self._tracker(self._prev, curr, pts)

        self._prev = curr

        return self._pts

    def show(self, w='pts'):
        tmp = gray2rgb(self._prev).copy()
        for pt in self._pts.astype(np.int32):
            cv2.circle(tmp, tuple(pt), 12, (255, 0, 0), -1)

        cv2.imshow(w, tmp)


if __name__ == '__main__':
    pass
