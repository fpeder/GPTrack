#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import cPickle as pickle


class MakeGt():

    def __init__(self):
        self._strum = []

    def run(self, vf, wait):
        vc = cv2.VideoCapture(vf)
        while vc.isOpened():
            try:
                ret, frame = vc.read()
                assert frame.any()
            except AttributeError:
                break

            cv2.imshow('frame', frame)
            key = cv2.waitKey(wait)
            if key == ord('q'):
                break
            elif key == ord('1'):
                print 'down'
                self._strum.append(-1)
            elif key == ord('0'):
                print 'up'
                self._strum.append(1)
            else:
                self._strum.append(0)

    def save(self, fn):
        if self._strum:
            with open(fn, 'w') as f:
                seq = np.array(self._strum)
                pickle.dump(seq, f)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="input video file")
    parser.add_argument("-o", "--outfile", type=str, help="output sequence")
    parser.add_argument("-w", '--wait', type=int, required=True)
    args = parser.parse_args()

    mgt = MakeGt()
    mgt.run(args.infile, args.wait)

    if args.outfile:
        mgt.save(args.outfile)
