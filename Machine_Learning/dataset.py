# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:56:21 2021

@author: kariln
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#DATAFRAME CREATION
def data_frame(filename: str):
    return pd.read_csv(filename, header = 0, sep=',', index_col=False)

def data_split(data):
    Y_col = ['T']
    X = data.drop(Y_col, axis=1) #Input dataframe, X
    Y = pd.DataFrame(data, columns=Y_col) #Output dataframe, Y

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, 
                                                        train_size=0.8,
                                                        test_size=0.2,
                                                        random_state=42)
    return X,Y,train_X, test_X, train_Y, test_Y

def X_Y_split(data):
    Y_col = ['T']
    X = data.drop(Y_col, axis=1) #Input dataframe, X
    Y = pd.DataFrame(data, columns=Y_col) #Output dataframe, Y
    return X,Y

#SEPARATION ON SPECIFIC LAYER NUMBER
def layer_split(data, layernum: int):
    for index, row in data.iterrows():
        if row['layerNum'] == layernum:
          t = row['t']
          break
    
    for index, row in data.iterrows():
        if row['t'] > t:
          i = index
          break
    train = data.iloc[:i-1,:] 
    test = data.iloc[i:,:]
    
    Y_col = ['T']
    train_X = train.drop(Y_col, axis=1)
    test_X = test.drop(Y_col, axis=1)
    train_Y = pd.DataFrame(train, columns=Y_col)
    test_Y = pd.DataFrame(test, columns=Y_col)
    return train_X, test_X, train_Y, test_Y
    
def column_drop(data, columns):
    return data.drop(columns = columns)

def equal_data_size(data1,data2):
    drop_columns_1 = np.setdiff1d(data1.columns.tolist(),data2.columns.tolist())
    data1 = column_drop(data1,drop_columns_1)
    drop_columns_2 = np.setdiff1d(data2.columns.tolist(),data1.columns.tolist())
    data2 = column_drop(data2,drop_columns_2)
    return data1, data2

#REMOVES CONSTANT COLUMNS IN DATAFRAME
def constant_removal(data):
    data_constant = data.columns[data.nunique() == 1]
    return data.drop(data_constant, axis = 1)

#SEPARATION IN SEPERATE LAYER DATASETS
def sep_layer_split(data):#must find out how to return the generated dataframes
    layer = min(data['layerNum'])
    nr_layers = max(data['layerNum'])
    datasets = []
    for  j in range(1,nr_layers):
      for index, row in data.iterrows():
          if row['layerNum'] > layer:
            t = row['t']
            break
    
      for index, row in data.iterrows():
          if row['t'] > t:
            i = index
            break
      globals()['layer%s' % j] = data.iloc[:i-1,:] 
      datasets.append(globals()['layer%s' % j])
      data = data.iloc[i:,:]
    globals()['layer%s' % nr_layers] = data.copy()
    
    
    Y_col = ['T']
    for  j in range(1,nr_layers+1):
      globals()['X_layer%s' % j] = globals()['layer%s' % j].drop(Y_col, axis=1)
      globals()['Y_layer%s' % j] = pd.DataFrame(globals()['layer%s' % j], columns=Y_col)
    return datasets

def label_test_split(data, labels):
    Y_col = ['T']
    df = data.loc[data['i'].isin(labels)]
    df = df.reset_index()
    df = df.drop(['index'], axis = 1)
    df_X = df.drop(Y_col, axis = 1)
    df_Y = pd.DataFrame(df, columns=Y_col)
    
    #train and validation dataset
    dt = data[data['i'] != 1]
    
    X,Y,train_X, test_X, train_Y, test_Y = data_split(dt)
    return X,Y,train_X, test_X, train_Y, test_Y, df, df_X,df_Y

