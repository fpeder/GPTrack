#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

from classifier import SkinClassifier
from features import Hist
from blockproc import BlockProcess

from sklearn.ensemble import RandomForestClassifier


def parse_config(conf):
    conf = yaml.load(open(conf, 'r'))
    model = eval(conf['model'])
    feat = [[eval(x['kind']), x['size'], eval(x['fun'])]
            for x in conf['features']]
    labels = {}
    for lab in conf['labels']:
        labels[str(lab['id'])] = lab['color']
    return model, labels, feat


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-c', '--config', type=str, required=True)
    args = parser.parse_args()

    path = args.db
    output = args.output
    configf = args.config

    assert os.path.exists(path), '!path...'
    assert os.path.exists(configf), '!config...'

    model, labels, feat = parse_config(configf)
    sc = SkinClassifier(model, labels, feat)
    sc.train(path, output=output)
