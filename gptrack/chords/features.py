#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Features():

    def __init__(self, size=(64, 64)):
        self._sz = size

    def run(self, X):
        nX1 = []
        for x in X:
            box = self.__crop_resize(x[0], x[2][1])
            vec = box.reshape(-1)
            vec -= vec.mean()
            vec = np.hstack((vec, x[2][0][1]))
            nX1.append(vec)

        return np.array(nX1)

    def __crop_resize(self, x, box):
        p, q = box[0], box[1]
        x = x[p[1]:q[1], p[0]:q[0]]
        x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        x = cv2.resize(x, self._sz)
        return x


if __name__ == '__main__':
    pass
