# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:09:26 2021

@author: kariln
THERMAL
"""

import numpy as np
import pandas as pd
from functions import column_check
from datetime import datetime

#INSERTING AMBIENT TEMPERATURE IF HISTORICAL DATA IS NOT AVAILABLE
def temp_history(data):
    now = datetime.now()
    print('Thermal history: ' + str(now))
    column_check(data,['T_1','T_2','T_3','T_4','T_5'])
    data['new'] = 0
    for index, row in data.iterrows():
      if row['T_5'] == str(None):
        data['T_5'].iloc[index] = np.float64(20.0)
        data['new'].iloc[index] = 5
      if row['T_4'] == str(None):
        data['T_4'].iloc[index] = np.float64(20.0)
        data['new'].iloc[index] = 4
      if row['T_3'] == str(None):
        data['T_3'].iloc[index] = np.float64(20.0)
        data['new'].iloc[index] = 3
      if row['T_2'] == str(None):
        data['T_2'].iloc[index] = np.float64(20.0)
        data['new'].iloc[index] = 2
      if row['T_1'] == str(None):
        data['T_1'].iloc[index] = np.float64(20.0)
        data['new'].iloc[index] = 1

    data[['T_1','T_2','T_3','T_4','T_5']] = data[['T_1','T_2','T_3','T_4','T_5']].fillna(20)
    data['T_1'] = pd.to_numeric(data['T_1'])
    data['T_2'] = pd.to_numeric(data['T_2'])
    data['T_3'] = pd.to_numeric(data['T_3'])
    data['T_4'] = pd.to_numeric(data['T_4'])
    data['T_5'] = pd.to_numeric(data['T_5'])
    data.to_csv('disp_Tt.csv',encoding='utf-8',  index=False) 
    return data

#ADDING TEMPERATURE GRADIENTS
def temp_grad(data):
    now = datetime.now()
    print('Thermal gradients: ' + str(now))
    column_check(data,['T_1','T_2','T_3','T_4','T_5'])
    data['dT_12'] = abs(data['T_1']-data['T_2'])
    data['dT_23'] = abs(data['T_2']-data['T_3'])
    data['dT_34'] = abs(data['T_3']-data['T_4'])
    data['dT_45'] = abs(data['T_4']-data['T_5'])
    data.to_csv('disp_grad.csv',encoding='utf-8',  index=False) 
    return data

#ADDING MELT POOL
def melt(data):
    now = datetime.now()
    print('Melt pool: ' + str(now))
    column_check(data,['T_1'])
    data['melt'] = None
    for index,row in data.iterrows():
      if row['T_1'] > 643:
        data['melt'].iloc[index] = 1
      else:
        data['melt'].iloc[index] = 0
    data.to_csv('disp_melt.csv',encoding='utf-8',  index=False) 
    return data

#INSERTING MEAN, MEDIAN AND PEAK TEMPERATURE FOR ALL NODES AT PREVIOUS TIMESTEP
def temp_stat(data):
    now = datetime.now()
    print('Thermal statistics: ' + str(now))
    column_check(data,['T_1','t'])
    num_t = data['t'].nunique()
    t = data['t'].unique()
    t_mean = []
    t_peak = []
    t_median = []
    data['T_mean'] = None
    data['T_median'] = None
    data['T_peak'] = None
    for i in range(0,num_t):
      data_t = data[data['t'] == t[i]] 
      t_mean.append(data_t['T_1'].mean())
      t_median.append(data_t['T_1'].median())
      t_peak.append(max(data_t['T_1']))
    
    for index,row in data.iterrows():
      i = np.where(t == row['t'])[0][0]
      data['T_mean'].iloc[index] = t_mean[i]
      data['T_median'].iloc[index] = t_median[i]
      data['T_peak'].iloc[index] = t_peak[i]
    data.to_csv('disp_T.csv',encoding='utf-8',  index=False) 
    return data

def thermal(data):
    data = temp_history(data)
    data = temp_grad(data)
    data = melt(data)
    data = temp_stat(data)
    return data