#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import ModelConfig, DataConfig, DbConfig
from data import DataHandler, DataBalancer
from blockproc import BlockProcess
from features import Hist

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


class SkinTrainer():

    def __init__(self, modconf, dataconf, dbconf):
        self._model = modconf.model
        self._config = {'model': modconf, 'data': dataconf}
        self._dh = DataHandler(dataconf, dbconf, modconf.features)

    def run(self):
        X, y = self._dh.run()
        if self._config['data'].balance:
            X, y = DataBalancer().run(X, y)

        self._model.fit(X, y)

    def save(self, fn):
        pass


if __name__ == '__main__':
    labels = {'0': [0, 0, 0], '1': [255, 0, 0], '2': [0, 0, 255]}
    model = RandomForestClassifier(min_samples_split=1, n_estimators=20)
    featdesc = [[BlockProcess, 8, Hist(16)]]

    modconf = ModelConfig(model, featdesc)
    dataconf = DataConfig(labels, ds=4, discard=None)
    dbconf = DbConfig('db')

    st = SkinTrainer(modconf, dataconf, dbconf)
    st.run()
