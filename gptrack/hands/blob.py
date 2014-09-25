#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from conncomp import ConnComps


class MyBlobDetector():

    def __init__(self, num_comp=2, min_elem=1500):
        self._nc = num_comp
        self._me = min_elem
        self._cc = ConnComps()

    def run(self, img):
        cc = self._cc.run(img)
        labels = np.unique(cc)[1:]
        pts, nelems, new_labels = [], [], []

        for label in labels:
            nelem = len(cc[cc == label])
            if nelem > self._me:
                (x, y) = np.where(cc == label)
                pt = np.mean(np.array([y, x]), axis=1)

                pts.append(pt)
                nelems.append(nelem)
                new_labels.append(label)

            else:
                cc[cc == label] = 0

        pts, labels = self.__get_biggest(pts, nelems, new_labels)
        mask = self.__get_mask(cc, labels)

        return mask, pts

    def __get_mask(self, cc, labels):
        mask = cc
        for lab in labels:
            mask[mask == lab] = 255
        mask[mask != 255] = 0

        return mask

    def __get_biggest(self, pts, nelems, idx):
        pts = np.array(pts)
        nelems = np.array(nelems)
        idx = np.array(idx)

        if self._nc and (len(nelems) >= self._nc):
            sort = np.argsort(-nelems)
            pts = pts[sort[0:self._nc], :]
            idx = idx[sort[0:self._nc]]

        return pts, idx


# class BlobDetector():

#     def __init__(self, method='dog', max_sigma=50, threshold=4):
#         self._method = method
#         self._ms = max_sigma
#         self._th = threshold
#         self._img = None
#         self._blobs = None

#     def run(self, img):
#         imgg = img
#         self._img = imgg

#         if self._method == 'dog':
#             blobs = blob_dog(imgg, max_sigma=self._ms, threshold=self._th)
#             self._blobs = blobs
#             blobs = np.array([[x[1], x[0], x[2]] for x in blobs if
#                               (x[0] > 0 and x[1] > 0)], np.float32)
#             blobs = blobs[-blobs[:, -1].argsort()][:, :-1]
#             blobs = np.array(blobs)

#         else:
#             pass

#         return blobs

#     def show(self):
#         tmp = cv2.cvtColor(self._img, cv2.COLOR_GRAY2BGR)
#         fig, ax = plt.subplots(1, 1)
#         ax.imshow(tmp, interpolation='nearest')
#         for blob in self._blobs:
#             y, x, r = blob
#             c = plt.Circle((x, y), r*1.4142, color='red', linewidth=2,
#                            fill=False)
#             ax.add_patch(c)
#         plt.show()
