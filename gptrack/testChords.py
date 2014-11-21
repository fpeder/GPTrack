#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt
import cPickle as pickle

from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report


X, y = pickle.load(open('chords.pck', 'r'))

Xtrain, Xtest, ytrain, ytest = cross_validation.train_test_split(
    X, y, test_size=0.4, random_state=0)

#lda = LDA(n_components=None, priors=None)
#lda = PCA(n_components=32)
#Xtrain = lda.fit_transform(Xtrain, ytrain)

#Xtest = lda.transform(Xtest)

cls = RandomForestClassifier(n_estimators=20)
#cls = ExtraTreesClassifier(n_estimators=20)
cls.fit(Xtrain, ytrain)

y = cls.predict(Xtest)
print cls.score(Xtest, ytest)
print confusion_matrix(ytest, y)

# tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
#                      'C': [1, 10, 100, 1000]},
#                     {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

# scores = ['precision', 'recall']

# for score in scores:
#     print("# Tuning hyper-parameters for %s" % score)
#     print()

#     clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring=score)
#     clf.fit(Xtrain, ytrain)

#     print("Best parameters set found on development set:")
#     print()
#     print(clf.best_estimator_)
#     print()
#     print("Grid scores on development set:")
#     print()
#     for params, mean_score, scores in clf.grid_scores_:
#         print("%0.3f (+/-%0.03f) for %r"
#               % (mean_score, scores.std() / 2, params))
#     print()

#     print("Detailed classification report:")
#     print()
#     print("The model is trained on the full development set.")
#     print("The scores are computed on the full evaluation set.")
#     print()
#     y_true, y_pred = ytest, clf.predict(Xtest)
#     print(classification_report(y_true, y_pred))
#     print()
