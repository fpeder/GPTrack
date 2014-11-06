#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from hands.skin.classifier import SkinClassifier

if __name__ == '__main__':
    import argparse
    from os.path import exists

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-c', '--config', type=str, required=True)
    args = parser.parse_args()

    output = args.output
    configf = args.config
    assert exists(configf), '!config...'

    config = Config()
    config.load(configf)

    st = SkinClassifier()
    st.train(config)
    st.save(output)
