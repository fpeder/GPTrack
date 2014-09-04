#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2


def mat2vec(x):
    return x.reshape((x.shape[0] * x.shape[1], x.shape[2]))


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
