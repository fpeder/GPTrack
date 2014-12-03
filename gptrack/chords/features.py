#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from cropHand import CropHand


class Features(object):

    def __init__(self):
        self._ch = CropHand()


class Chord2Vec(Features):

    def __init__(self):
        Features.__init__(self)

    def run(self, frame, mask, box):
        img = self._ch.run(frame, mask, box)
        vec = img.reshape(-1)
        vec -= vec.mean()
        vec = np.hstack((vec, box[1]))
        return vec


if __name__ == '__main__':
    import cPickle as pickle

    img = 'chords/tmp/frame.Am7_n.200.jpg'
    info = 'chords/tmp/info.Am7_n.200.pck'
    mask = 'chords/tmp/mask.Am7_n.200.jpg'

    img = cv2.imread(img)
    mask = cv2.imread(mask)
    info = pickle.load(open(info, 'r'))
