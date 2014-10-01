#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class ConnComps():

    def __init__(self, num=-1):
        pass

    def run(self, img):
        label = np.int32(img.copy())
        ncomp = 1
        while True:
            pt = self.__find_seed(label)
            if not pt:
                break
            cv2.floodFill(label, None, pt, ncomp)
            ncomp += 1
        return label

    def __find_seed(self, img):
        tmp = np.where(img == 255)
        pt = ()
        if tmp[0].any() and tmp[1].any():
            pt = (tmp[1][0], tmp[0][0])
        return pt


if __name__ == '__main__':
    pass
