#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import cPickle as pickle


class Hands():

    def __init__(self, comps):
        if len(comps) != 2:
            self._left = None
            self._right = None
        else:
            self._left = Hand(comps[0])
            self._right = Hand(comps[1])
            self.__sort()

    def __sort(self):
        if self._left.cent[0] < self._right.cent[0]:
            self._left, self._right = self._right, self._left

    def valid(self):
        return self._left and self._right

    def get_points(self):
        return [self._left.cent, self._right.cent]

    def save(self, fn):
        with open(fn, 'w') as f:
            pickle.dump({'left': self._left, 'right': self._right}, f)

    def show(self):
        tmp = self._left.show()
        tmp += self._right.show()
        return tmp

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class Hand():

    def __init__(self, comp, f=0.4):
        self._break_factor = f
        self._cent = comp.cent.astype(np.int32)
        self._box = [x.astype(np.int32) for x in comp.box]
        self._mask = np.zeros((360, 640), np.uint8)
        self._mask[comp.idx] = 255

        p1, p2 = self._box
        height = np.abs(p1[1] - p2[1])
        if height > self._break_factor * 360:
            x, y = self._cent
            self._mask[0:x, 0:y] = 0
            (x, y) = np.where(self._mask == 255)
            self._cent = np.array([y, x]).mean(axis=1)

    def show(self):
        tmp = cv2.cvtColor(self._mask, cv2.COLOR_GRAY2BGR)

        pt1 = (self._box[0][0], self._box[0][1])
        pt2 = (self._box[1][0], self._box[1][1])
        cv2.rectangle(tmp, pt1, pt2, (255, 0, 0))

        pt = (np.int32(self._cent[0]), np.int32(self._cent[1]))
        cv2.circle(tmp, pt, 10, (0, 0, 255), -1)

        return tmp

    @property
    def cent(self):
        return self._cent

    @property
    def box(self):
        return self._box

    @property
    def mask(self):
        return self._mask
