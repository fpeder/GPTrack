#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os


class FrameReader():

    def __init__(self, video):
        assert os.path.exists(video), '! video ...'
        self._vc = cv2.VideoCapture(video)

    def next(self):
        while self._vc.isOpened():
            _, frame = self._vc.read()
            try:
                assert frame.any()
            except AttributeError:
                break

            yield frame
