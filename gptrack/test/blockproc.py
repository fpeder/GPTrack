#!/usr/env/python
# -*- coding: utf-8 -*-

import numpy as np

from progressbar import ProgressBar


class BlockProcess():

    def __init__(self, w, feat):
        self._w = w
        self._feat = feat

    def run(self, img):
        M, N = img.shape[:-1]
        L = self._feat.length
        dst = np.zeros((M, N, L), dtype=np.float)

        pbar = ProgressBar(maxval=M*N)
        pbar.start()
        count = 0

        for i in np.arange(0, M):
            for j in np.arange(0, N):
                self.__compute(img, dst, i, j)

                count += 1
                pbar.update(count)

        pbar.finish()

        return dst

    def __compute(self, src, dst, i, j):
        block = self.__get_block(src, i, j)
        dst[i, j, :] = self._feat.run(block)

    def __get_block(self, src, i, j):
        M, N = src.shape[:-1]
        si = i - self._w/2 if i - self._w/2 >= 0 else 0
        ei = i + self._w/2 if i + self._w/2 < M else M
        sj = j - self._w/2 if j - self._w/2 >= 0 else 0
        ej = j + self._w/2 if j + self._w/2 < N else N
        return src[si:ei, sj:ej]


if __name__ == '__main__':
    pbar = ProgressBar(maxval=10000000).start()
    for i in range(1000000):
        pbar.update(10*i+1)
    pbar.finish()
