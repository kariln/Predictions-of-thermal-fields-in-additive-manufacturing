# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:44:27 2021

@author: kariln
"""

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import math
import numpy as np

def r2(y_true,y_pred):
    return roundup(r2_score(y_true,y_pred))

def roundup(a, digits=4):
    n = 10**-digits
    return round(math.ceil(a / n) * n, digits)

def r2_adjust(test_X,r2_score):
  return 1-(1-r2_score)*((test_X.shape[0]-1)/(test_X.shape[0]-test_X.shape[1]-1))

def average(lst): 
    return sum(lst) / len(lst) 

def mape(y_true, y_pred):
  return roundup(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)

def mae(y_true,y_pred):
    return roundup(mean_absolute_error(y_true,y_pred))

def percentage_error(actual, predicted):
    res = np.empty(actual.shape)
    for j in range(actual.shape[0]):
        if actual[j] != 0:
            res[j] = (actual[j] - predicted[j]) / actual[j]
        else:
            res[j] = predicted[j] / np.mean(actual)
    return res

def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs(percentage_error(np.asarray(y_true), np.asarray(y_pred)))) * 100

def nmse(actual: np.ndarray, predicted: np.ndarray):
    """ Normalized Root Mean Squared Error """
    return mse(actual, predicted) / (actual.max() - actual.min())

def mse(y_true,y_pred):
    return roundup(mean_squared_error(y_true,y_pred))

def rmse(y_true,y_pred):
    return mse(y_true,y_pred)


def nrmse(actual: np.ndarray, predicted: np.ndarray):
    """ Normalized Root Mean Squared Error """
    return rmse(actual, predicted) / (actual.max() - actual.min())