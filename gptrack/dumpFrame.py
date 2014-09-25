#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os


class DumpFrame():

    def __init__(self, src, dst, nskip=5000, fps=25):
        self._src = src
        self._dst = dst
        self._nskip = nskip
        self._fps = fps

    def run(self):
        vc = cv2.VideoCapture(self._src)
        dst = self._dst + os.path.basename(self._src)
        count = 0

        while vc.isOpened():
            ret, frame = vc.read()

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1000/self._fps)

            if key == ord('s'):
                out = dst + "." + str(count) + ".jpg"
                print out
                cv2.imwrite(out, frame)
                count += 1

            if key == ord('q'):
                break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="inout video file")
    parser.add_argument("-d", "--dstdir", type=str, required=True,
                        help="direcotry where to save frames")
    args = parser.parse_args()

    df = DumpFrame(args.infile, args.dstdir)
    df.run()
