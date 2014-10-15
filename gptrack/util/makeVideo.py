#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


class MakeVideo():
    UP = 1
    DOWN = -1

    def __init__(self):
        self._colors = {'UP': (255, 0, 0), 'DOWN': (0, 0, 255)}

    def run(self, video, seq, updown, dest):
        vc, i, out = cv2.VideoCapture(video), 0, []
        while vc.isOpened():
            try:
                ret, frame = vc.read()
                assert frame.any()
            except AttributeError:
                break

            if updown[i] == self.UP:
                out = self.__draw(frame, seq[i, :], 'UP')
            elif updown[i] == self.DOWN:
                out = self.__draw(frame, seq[i, :], 'DOWN')
            else:
                out = frame

            outfile = os.path.join(dest, str(i) + '.jpg')
            cv2.imwrite(outfile, out)
            i += 1

    def __draw(self, img, pt, x):
        pt = tuple(pt.astype(np.int32))
        cv2.circle(img, pt, 10, self._colors[x], -1)
        return img


if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=str, required=True)
    parser.add_argument('-s', '--seq', type=str, required=True)
    parser.add_argument('-u', '--updown', type=str, required=True)
    parser.add_argument('-d', '--dest_dir', type=str, required=True)
    args = parser.parse_args()

    video, seq, updown, dest = args.video, args.seq, args.updown, args.dest_dir
    assert os.path.exists(video), 'video'
    assert os.path.exists(seq), 'seq'
    assert os.path.exists(updown), 'updown'
    assert os.path.exists(dest), 'dest'

    seq = pickle.load(file(seq))
    updown, _ = pickle.load(file(updown))

    mv = MakeVideo()
    mv.run(video, seq, updown, dest)
