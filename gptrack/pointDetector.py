#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blobDetector import MyBlobDetector


class PointDetector():

    def __init__(self, num_comp=2):
        self._bd = MyBlobDetector(num_comp=num_comp)

    def run(self, img):
        return self._bd.run(img)

if __name__ == '__main__':
    pass
