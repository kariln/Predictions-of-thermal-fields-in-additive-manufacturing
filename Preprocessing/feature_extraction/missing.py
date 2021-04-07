# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:30:45 2021

@author: kariln
REMOVAL OF MISSING DATAPOINTS
"""
import numpy as np


#MISSING DATA POINTS
def missing_data(data):
    data[data==np.inf]=np.nan #replaces inf with nan
    print(data.head())
    print("There are " + str(data.isnull().sum()) + "rows with missing values.")
    data = data.dropna() #imputation
    data = data.drop_duplicates(keep="first")
    return data