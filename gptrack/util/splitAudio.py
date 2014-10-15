#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os


class SplitAudio():
    FFMPEG = 'ffmpeg'
    ACODEC = 'wav'

    def __init__(self, src, dst, fps=100):
        self._src = src
        self._dst = dst
        self._fps = fps

    def run(self, updown, frame):
        count = 0
        fn = self.__make_fn()

        for start, time in self.__get_times(updown, frame):
            outfile = fn + '.' + str(count) + '.' + self.ACODEC
            outfile = os.path.join(self._dst, outfile)

            cmd = self.FFMPEG + " -i " + self._src + " -ss " + str(start) + " -t " + str(time) + " -f wav " + outfile

            os.system(cmd)

            count += 1

    def __make_fn(self):
        tmp = os.path.basename(self._src)
        fn = "".join(tmp.split('.')[0:-1])
        return fn

    def __get_times(self, updown, frame):
        idx = np.where(updown != 0)[0]
        start, time = frame[idx], np.diff(frame[idx])
        start = np.around(start[:-1] * 1./self._fps, decimals=2)
        time = np.around(time * 1./self._fps, decimals=2)
        return zip(start, time)


if __name__ == '__main__':
    import argparse
    import cPickle as pickle

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video_in', type=str, required=True)
    parser.add_argument('-i', '--updown', type=str, required=True)
    parser.add_argument('-o', '--output_dir', type=str, required=True)
    args = parser.parse_args()

    updown, frame = pickle.load(file(args.updown))
    src, dst = args.video_in, args.output_dir
    assert os.path.exists(src), 'src'
    assert os.path.exists(dst), 'dst'

    sa = SplitAudio(src, dst)
    sa.run(updown, frame)
