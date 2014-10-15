#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os


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


class DumpVideo():

    def __init__(self):
        pass

    def run(self, dest, fn):
        vc, count = cv2.VideoCapture(fn), 0
        while vc.isOpened():
            try:
                _, frame = vc.read()
                assert frame.any()
            except AttributeError:
                break

            outfile = os.path.join(dest, fix(count))
            cv2.imwrite(outfile, frame)
            count += 1

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=str, required=True)
    parser.add_argument('-d', '--dest_dir', type=str, required=True)
    args = parser.parse_args()

    video, dest = args.video, args.dest_dir
    assert os.path.exists(video), 'video'
    assert os.path.exists(dest), 'dest'

    dump = DumpVideo()
    dump.run(dest, video)
