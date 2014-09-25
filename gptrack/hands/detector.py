#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blob import MyBlobDetector


class PointDetector():

    def __init__(self, num_comp=2, min_elem=2500):
        self._bd = MyBlobDetector(num_comp=num_comp, min_elem=min_elem)

    def run(self, img):
        return self._bd.run(img)

if __name__ == '__main__':
    pass
