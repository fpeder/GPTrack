#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import label


class ChordClassifier():

    def __init__(self):
        pass

    def run(self, img, hand):
        p, q = hand.box
        
        tmp = img[p[1]:q[1], p[0]:q[0]].copy()
        mask = hand.mask[p[1]:q[1], p[0]:q[0]].copy()

        fg = cv2.erode(mask, None,iterations = 5)
        bgt = cv2.dilate(mask,None,iterations = 10)
        ret,bg = cv2.threshold(bgt,1,128,1)
        marker = cv2.add(fg,bg)
        marker32 = np.int32(marker)
        cv2.watershed(tmp,marker32)
        m = cv2.convertScaleAbs(marker32)


        import pdb; pdb.set_trace()

        return tmp1



if __name__ == '__main__':
    pass
