#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blob import MyBlobDetector
from skin.classifier import SkinClassifier
from skin.enhancer import SkinEnhancer
from hands import Hands


class HandsDetector():

    def __init__(self, model, cls=SkinClassifier(), ench=SkinEnhancer(),
                 min_elem=2000):
        self._cls = cls
        self._cls.load(model)
        self._ench = ench
        self._db = MyBlobDetector(num_comp=2, min_elem=min_elem)

    def run(self, frame):
        skin, mask = self._cls.run(frame)
        mask = self._ench.run(mask)
        comps = self._db.run(mask)
        hands = Hands(comps)
        return hands


if __name__ == '__main__':
    pass
