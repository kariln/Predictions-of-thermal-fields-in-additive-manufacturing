# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:30:45 2021

@author: kariln
REMOVAL OF MISSING DATAPOINTS
"""
import numpy as np
from datetime import datetime


#MISSING DATA POINTS
def missing_data(data):
    now = datetime.now()
    print('Missing data: ' + str(now))
    data[data==np.inf]=np.nan #replaces inf with nan
    print(data.head())
    print("There are " + str(data.isnull().sum()) + "rows with missing values.")
    data = data.dropna() #imputation
    return data

def duplicate_data(data):
    now = datetime.now()
    print('Duplicate data: ' + str(now))
    data = data.drop_duplicates(keep="first")
    return data
    
def improve(data):
    data = missing_data(data)
    data = duplicate_data(data)
    return data