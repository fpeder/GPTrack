#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from cropHand import CropHand
from progress.bar import Bar


class Features():

    def __init__(self):
        self._ch = CropHand()

    def run(self, X):
        nX1 = []
        bar = Bar('Processing', max=len(X))
        for x in X:
            box = self._ch.run(x[0], x[1], x[2][1])
            vec = box.reshape(-1)
            vec -= vec.mean()
            vec = np.hstack((vec, x[2][0][1]))
            nX1.append(vec)
            bar.next()
        bar.finish()
        return np.array(nX1)


if __name__ == '__main__':
    import cPickle as pickle

    img = 'chords/tmp/frame.Am7_n.200.jpg'
    info = 'chords/tmp/info.Am7_n.200.pck'
    mask = 'chords/tmp/mask.Am7_n.200.jpg'

    img = cv2.imread(img)
    mask = cv2.imread(mask)
    info = pickle.load(open(info, 'r'))
