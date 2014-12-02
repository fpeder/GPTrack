#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt
import cPickle as pickle
import gzip

from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB


X, y = pickle.load(gzip.open('chords.pckz', 'rb'))

#Xtrain, Xtest, ytrain, ytest = cross_validation.train_test_split(
#    X, y, test_size=0.5, random_state=0)

#lda = LDA(n_components=None, priors=None)
#lda = PCA(n_components=32)
#Xtrain = lda.fit_transform(Xtrain, ytrain)

#Xtest = lda.transform(Xtest)

#cls = RandomForestClassifier(n_estimators=20)
cls = MultinomialNB()
#cls = ExtraTreesClassifier(n_estimators=20)
#cls.fit(Xtrain, ytrain)

#y = cls.predict(Xtest)

#print cls.score(Xtest, ytest)
#print confusion_matrix(ytest, y)

kf = cross_validation.KFold(len(y), n_folds=3, random_state=0, shuffle=True)

score = []
for train_index, test_index in kf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    cls.fit(X_train, y_train)
    score.append(cls.score(X_test, y_test))

print np.array(score).mean()
