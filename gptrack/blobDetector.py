#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pylab as plt

from skimage.feature import blob_dog


class BlobDetector():

    def __init__(self, method='dog', max_sigma=50, threshold=4):
        self._method = method
        self._ms = max_sigma
        self._th = threshold
        self._img = None
        self._blobs = None

    def run(self, img):
        if len(img.shape) == 3:
            self._img = img
            imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            imgg = self._preprocess(img)
            self._img = cv2.cvtColor(imgg, cv2.COLOR_GRAY2BGR)

        if self._method == 'dog':
            blobs = blob_dog(imgg, max_sigma=self._ms, threshold=self._th)
            self._blobs = blobs
            blobs = np.array([[x[1], x[0], x[2]] for x in blobs if x[0] > 0 and
                              x[1] > 0], np.float32)
            blobs = blobs[-blobs[:, -1].argsort()][:, :-1]
            blobs = np.array(blobs)

        else:
            pass

        return blobs

    def _preprocess(self, img):
        img = cv2.medianBlur(img, 5)
        kernel = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    def show(self):
        image = self._img
        fig, ax = plt.subplots(1, 1)
        ax.imshow(image, interpolation='nearest')
        for blob in self._blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r*1.4142, color='red', linewidth=2,
                           fill=False)
            ax.add_patch(c)
        plt.show()
