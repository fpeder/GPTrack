#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class SkinEnhancer():

    def __init__(self, mks=7, cks=(10, 10)):
        self._mks = mks
        self._ks = np.ones(cks, np.uint8)

    def run(self, img):
        out = cv2.medianBlur(img, self._mks)
        out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, self._ks)

        return out


if __name__ == '__main__':
    pass
