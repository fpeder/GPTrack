#!/usr/bin/env python
# -*- coding: utf-8 -*-


def makeCallableString(desc):
    method, params = desc
    param = []
    for key in params.keys():
        param.append(key + '=' + str(params[key]))
    param = ','.join(param)
    tmp = method + '(' + param + ')'
    return tmp
