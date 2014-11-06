#!/usr/bin/env python
# -*- coding: utf-8 -*-


from data import DataHandler, DataBalancer
from util import makeCallableString

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from os.path import exists


class SkinClassifier():

    def __init__(self):
        self._cls = None
        self._dh = None

    def train(self, config):
        self._cls = self.__parse(config.model.cls)
        self._dh = DataHandler(config.data, config.db, config.model.features)
        X, y = self._dh.run()
        if config.data.balance:
            X, y = DataBalancer().run(X, y)

        self._cls.fit(X, y)

    def run(self, img):
        M, N = img.shape[:-1]
        X = self._dh.get_features(img)
        y = self._cls.predict(X)
        y = self._dh.reshape(y, M, N)
        import pdb; pdb.set_trace()
        

    def save(self, fn):
        joblib.dump((self._cls, self._dh), fn)

    def load(self, fn):
        assert exists, '!fn...'
        self._cls, self._dh = joblib.load(fn)

    def __parse(self, desc):
        tmp = makeCallableString(desc)
        return eval(tmp)


if __name__ == '__main__':
    import cv2
    # modconf = ModelConfig(model, featdesc)
    # dataconf = DataConfig(labels, ds=4, discard=None)
    # dbconf = DbConfig('db')

    # st = SkinTrainer(modconf, dataconf, dbconf)
    # st.run()

    img = cv2.imread('db/2.jpg')
    assert img.any(), '!img...'

    sc = SkinClassifier()
    sc.load('model/asd.pkl')
    sc.run(img)
