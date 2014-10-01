#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class PointTracker():

    def __init__(self, prev, pts, tracker=cv2.calcOpticalFlowPyrLK):
        self._prev = prev
        self._pts = np.array(pts)
        self._tracker = tracker

    def run(self, curr):
        if len(curr.shape) == 3:
            curr = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        if self._prev.any() and self._pts.any():
            pts = self._pts.astype(np.float32)
            self._pts, _, _ = self._tracker(self._prev, curr, pts)

        self._prev = curr
        return self._pts


if __name__ == '__main__':
    pass
