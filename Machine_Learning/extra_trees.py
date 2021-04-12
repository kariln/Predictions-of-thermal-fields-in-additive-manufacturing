# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 21:05:34 2021

@author: kariln
"""
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import cross_val_score
import scikitplot as skplt
import matplotlib.pyplot as plt

def extra_trees(nr_estimators: int, train_X, train_Y, test_X, test_Y, metric: str):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    predicted = et_500.predict(test_X)
    train_scores = cross_val_score(et_500, train_X, train_Y, cv=5, scoring=metric)
    test_scores = cross_val_score(et_500, test_X, test_Y, cv=5, scoring=metric)
    return predicted, train_scores, test_scores

def feature_importance(model, train_X):
    nr_features = train_X.shape[1]
    skplt.estimators.plot_feature_importances(model,text_fontsize=16,max_num_features=nr_features,figsize=(30,4),feature_names=train_X.columns)
    plt.xticks(rotation=90, fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.title('Feature importance', fontsize = 30)
    plt.savefig('feature_importance', bbox_inches = "tight")
    plt.show()