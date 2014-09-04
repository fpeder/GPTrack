#!/usr/bin/env python
# -*- coding: utf-8 -*-

from skinClassifier import SkinClassifier

if __name__ == '__main__':
    import cv2
    import sys
    import pylab as plt

    if len(sys.argv) != 2:
        print 'error: ./... <img>'
        sys.exit(-1)

    sc = SkinClassifier()
    sc.load('data/model/forest.pkl')

    img = cv2.imread(sys.argv[1])
    skin, mask = sc.run(img)

    plt.imshow(skin)
    plt.show()
