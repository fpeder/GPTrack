#!/usr/env/bin python
# -*- coding: utf-8 -*-

import numpy as np
import cv2


class SkinFill():
    COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128)]

    def __init__(self, lth=(8, )*3, hth=(20, )*3):
        self._lth = lth
        self._hth = hth

    def run(self, img, pts):
        for i in range(pts.shape[0]):
            pt = tuple(pts[i].astype(np.int32))
            if (pt[0] < 0 or pt[1] < 0 or pt[0] > img.shape[1] or
                pt[1] > img.shape[0]):
                continue
            cv2.floodFill(img, None, pt,
                          self.COLORS[np.mod(i, len(self.COLORS))],
                          self._lth, self._hth)
        return img
