#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


def hist1ch(x, ch, nbins=[255], interval=[1, 255]):
    return cv2.calcHist([x], [ch], None, nbins, interval)


def rgb2gray(x):
    return cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)


def gray2rgb(x):
    return cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)


def rgb2ycrcb(x):
    return cv2.cvtColor(x, cv2.COLOR_BGR2YCR_CB)


def mat2vec(x):
    x = x.astype(np.double)
    if len(x.shape) == 3:
        x = x.reshape((x.shape[0] * x.shape[1], x.shape[2]))
    else:
        x = x.reshape((x.shape[0] * x.shape[1], 1))

    return x


def load_as_features(x):
    x = cv2.imread(x)
    x = cv2.cvtColor(x, cv2.COLOR_BGR2YCR_CB)

    return mat2vec(x)


def load_as_labels(x):
    y = cv2.imread(x, 0)
    y = y.reshape((y.shape[0] * y.shape[1], ))
    y[y == 255] = 0
    y[y > 0] = 1

    return y
