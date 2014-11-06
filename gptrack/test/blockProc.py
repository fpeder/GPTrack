#!/usr/env/bin python
# -*- coding: utf-8 -*-

import numpy as np
import ctypes as ct

from numpy.ctypeslib import ndpointer

_blockproc = np.ctypeslib.load_library('blockProc', '.')
_blockproc.hist.restype = ct.c_int

M = 4
N = 4
x = np.zeros((M, N, 3), np.int32)

x[0, 0, 0] = -1;
x[0, 0, 1] = 1;
x[0, 0, 2] = 2;

print x.shape
print x.ndim

_blockproc.hist.argtypes = [ndpointer(dtype=np.int32, shape=(M, N, 3))]
_blockproc.hist(x, M, N, 3)
