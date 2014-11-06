import cv2
import numpy as np
import sys

from blockproc import blocketize, blockHist


img = cv2.imread('db/2.jpg')

img = np.int32(img)
M, N, nch = img.shape
w = 8
s = int(sys.argv[1])
nbins = 10

C = np.ceil((M-w)/float(s)) * np.ceil((N-w)/float(s))

blocks = np.zeros((C, nch*nbins), np.int32)
blockHist(img, blocks, w, s, 10)

print blocks
