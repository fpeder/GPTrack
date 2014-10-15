#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

GRAY = cv2.CV_LOAD_IMAGE_GRAYSCALE


def fix(count):
    if count < 10:
        fn = '000' + str(count) + '.jpg'
    elif count >= 10 and count <= 99:
        fn = '00' + str(count) + '.jpg'
    elif count >= 100 and count <= 999:
        fn = '0' + str(count) + '.jpg'
    else:
        fn = str(count) + '.jpg'
    return fn


class Overlay():
    UP, DOWN = 1, -1

    def __init__(self, src, nframe=30, r=None):
        self._src = src
        self._nf = nframe
        self._r = r
        self._colors = {'1': (255, 0, 0), '-1': (0, 0, 255)}
        self._mask = {'1': cv2.imread('data/up.png', GRAY),
                      '-1': cv2.imread('data/down.png', GRAY)}

    def run(self, seq, updown):
        for s in [self.UP, self.DOWN]:
            for i in np.where(updown == s)[0]:
                for x in i + np.arange(-self._nf, self._nf):

                    if x < 0 or x > len(updown):
                        continue

                    img = self.__load(x)
                    mask = self._mask[str(s)]
                    img[mask > 0] = self._colors[str(s)]

                    #pt = tuple(seq[x, :].astype(np.int32))
                    #self.__draw(img, pt, s)

                    self.__save(img, x)

    def __load(self, i):
        img = os.path.join(self._src, fix(i))
        assert os.path.exists(img), 'img'
        return cv2.imread(img)

    def __save(self, img, i):
        fn = os.path.join(self._src, fix(i))
        cv2.imwrite(fn, img)

    def __draw(self, img, pt, x):
        cv2.circle(img, pt, self._r, self._colors[str(x)], -1)


if __name__ == '__main__':
    import argparse
    import os
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--src_dir', type=str, required=True)
    parser.add_argument('-s', '--seq', type=str, required=True)
    parser.add_argument('-i', '--updown', type=str, required=True)
    args = parser.parse_args()

    src, seq, updown = args.src_dir, args.seq, args.updown
    assert os.path.exists(src), 'dir'
    assert os.path.exists(seq), 'seq'
    assert os.path.exists(updown), 'updown'

    seq = pickle.load(file(seq))
    updown, _ = pickle.load(file(updown))

    o = Overlay(src, 30, 18)
    o.run(seq, updown)
