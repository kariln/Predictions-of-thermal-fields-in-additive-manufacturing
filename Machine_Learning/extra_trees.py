# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 21:05:34 2021

@author: kariln
"""
import sys
sys.path.append(r'C:\Users\kariln\Documents\GitHub\Master\Preprocessing')
sys.path.append(r'C:\Users\kariln\Documents\GitHub\Master\Machine_Learning')
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import cross_val_score
import scikitplot as skplt
import matplotlib.pyplot as plt
from feature_extraction.material import material,specific_heat
from feature_extraction.heat import beta,P_inst, P_inf
from feature_extraction.thermal import melt,temp_grad
from dataset import data_frame
import pandas as pd
from sklearn.metrics import mean_squared_error
from functions import column_check
import numpy as np

def extra_trees(nr_estimators: int, train_X, train_Y, test_X, test_Y, metric: str):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    predicted = et_500.predict(test_X)
    train_scores = cross_val_score(et_500, train_X, train_Y, cv=5, scoring=metric)
    test_scores = cross_val_score(et_500, test_X, test_Y, cv=5, scoring=metric)
    return predicted, train_scores, test_scores

def extra_tree_model(nr_estimators: int, train_X, train_Y):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    return et_500

def feature_importance(model, train_X):
    nr_features = train_X.shape[1]
    skplt.estimators.plot_feature_importances(model,text_fontsize=16,max_num_features=nr_features,figsize=(30,4),feature_names=train_X.columns)
    plt.xticks(rotation=90, fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.title('Feature importance', fontsize = 30)
    plt.savefig('feature_importance', bbox_inches = "tight")
    plt.show()
    
def node_predict(df_X_pred, model):  
  conductivity = pd.read_csv('AA2319_Conductivity.txt', names=["T","K"])
  specificHeat = pd.read_csv('AA2319_SpecificHeat.txt', names=["T","cp"])
  density = pd.read_csv('AA2319_Density.txt', names=["rho"])
  #problem med at man sender inn array istedenfor frame - muligens hent columns finn index of ersattt verdi
  predicted = []

  for i, row in df_X_pred.iterrows():
    if i == 0:
      row['T_1']  = 20
      row['T_2']  = 20
      row['T_3']  = 20
      row['T_4']  = 20
      row['T_5']  = 20
      row['new']  = 1
    elif i == 1:
      row['T_1']  = predicted[i-1]
      row['T_2']  = 20
      row['T_3']  = 20
      row['T_4']  = 20
      row['T_5']  = 20
      row['new']  = 2
    elif i == 2:
      row['T_1']  = predicted[i-1]
      row['T_2']  = predicted[i-2]
      row['T_3']  = 20
      row['T_4']  = 20
      row['T_5']  = 20
      row['new']  = 3
    elif i == 3:
      row['T_1']  = predicted[i-1]
      row['T_2']  = predicted[i-2]
      row['T_3']  = predicted[i-3]
      row['T_4']  = 20
      row['T_5']  = 20
      row['new']  = 4
    elif i == 4:
      row['T_1']  = predicted[i-1]
      row['T_2']  = predicted[i-2]
      row['T_3']  = predicted[i-3]
      row['T_4']  = predicted[i-4]
      row['T_5']  = 20
      row['new']  = 5
    else:
      row['T_1']  = predicted[i-1]
      row['T_2']  = predicted[i-2]
      row['T_3']  = predicted[i-3]
      row['T_4']  = predicted[i-4]
      row['T_5']  = predicted[i-5]
      row['new']  = 0
    
    #updating features dependent on T_1
    sub_dataframe = df_X_pred.iloc[[i], :]
    sub_dataframe = sub_dataframe.reset_index()
    sub_dataframe = sub_dataframe.drop(columns=['index'])
    
    #Material
    sub_dataframe = material(sub_dataframe,density,specificHeat,conductivity).iloc[[0], :]
    df_X_pred['density'].iloc[i] = sub_dataframe['density'].iloc[0]
    df_X_pred['K'].iloc[i] = sub_dataframe['K'].iloc[0]
    df_X_pred['cp'].iloc[i] = sub_dataframe['cp'].iloc[0]
    df_X_pred['diffusivity'].iloc[i] = sub_dataframe['diffusivity'].iloc[0]
    
    #Heat
    sub_dataframe = beta(sub_dataframe).iloc[[0], :]
    df_X_pred['beta'].iloc[i] = sub_dataframe['beta'].iloc[0]
    
    sub_dataframe = P_inst(sub_dataframe).iloc[[0], :]
    df_X_pred['P_inst'].iloc[i] = sub_dataframe['P_inst'].iloc[0]
    
    sub_dataframe = melt(sub_dataframe).iloc[[0], :]
    df_X_pred['melt'].iloc[i] = sub_dataframe['melt'].iloc[0]
    
    sub_dataframe = temp_grad(sub_dataframe).iloc[[0], :]
    df_X_pred['dT_12'].iloc[i] = sub_dataframe['dT_12'].iloc[0]
    df_X_pred['dT_23'].iloc[i] = sub_dataframe['dT_23'].iloc[0]
    df_X_pred['dT_34'].iloc[i] = sub_dataframe['dT_34'].iloc[0]
    df_X_pred['dT_45'].iloc[i] = sub_dataframe['dT_45'].iloc[0]

    predict = model.predict(row.values.reshape(1,-1))
    predicted.append(predict[0])
  return df_X_pred,predicted

def test_predict(df_X,model):
    labels = df_X['i'].unique()
    df_X['T_pred'] = -99
    df_X['density'] = -99
    df_X['cp'] = -99
    df_X['K'] = -99
    df_X['diffusivity'] = -99
    df_X['beta'] = -99
    df_X['P_inst'] = -99
    df_X['melt'] = -99
    df_X['dT_12'] = -99
    df_X['dT_23'] = -99
    df_X['dT_34'] = -99
    df_X['dT_45'] = -99
    for label in labels:
      label_set = df_X[df_X['i'] == label]
      df_X_reset = label_set.reset_index()
      df_X_pred = df_X_reset.drop(columns=['index','T_pred'])
      df_X_pred,predicted = node_predict(df_X_pred,model)
      for i,r in df_X_pred.iterrows():
        index = df_X_reset['index'].iloc[i]
        df_X['T_1'].iloc[index] = r['T_1']
        print(df_X['T_1'].iloc[index] - r['T_1'])
        df_X['T_2'].iloc[index] = r['T_2']
        df_X['T_3'].iloc[index] = r['T_3']
        df_X['T_4'].iloc[index] = r['T_4']
        df_X['T_5'].iloc[index] = r['T_5']
        df_X['new'].iloc[index] = r['new']
        df_X['density'].iloc[index] = r['density']
        df_X['K'].iloc[index] = r['K']
        df_X['cp'].iloc[index] = r['cp']
        df_X['diffusivity'].iloc[index] = r['diffusivity']
        df_X['beta'].iloc[index]=r['beta']
        df_X['P_inst'].iloc[index] = r['P_inst']
        df_X['melt'].iloc[index] = r['melt']
        df_X['dT_12'].iloc[index] = r['dT_12']
        df_X['dT_23'].iloc[index] = r['dT_23']
        df_X['dT_34'].iloc[index] = r['dT_34']
        df_X['dT_45'].iloc[index]=r['dT_45']
        df_X['T_pred'].iloc[index] = predicted[i]
    return df_X

def node_predict_plot(predicted,df_Y,df_X):
    delta = []
    label = df_X['i'].iloc[0]
    for i in range(0,len(df_Y.values.tolist())):
      delta.append((df_Y.values.tolist()[i]-predicted[i]))
    
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(9, 9))
    fig.suptitle('Prediction of thermal profile, node' + str(label), fontsize=16)
    ax1.plot(df_X['t'], predicted, label='Predicted', color = 'blue')
    ax1.scatter(df_X['t'], df_Y, label = 'True', color = 'orange')
    ax1.legend()
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature[$C^\circ$]')
    
    ax2.plot(df_X['t'], delta, color = "r", label="Delta = true value - predicted value")
    ax2.set_ylabel('Temperature[$C^\circ$]')
    ax2.legend()
    plt.show()
    
def node_performance(df_X,df_Y):
    column_check(df_X,['T_pred'])
    labels = df_X['i'].unique()
    df_X['T'] = df_Y['T']
    data = pd.DataFrame(columns=['i','mse'])
    for label in labels:
      label_set = df_X[df_X['i'] == label]
      mse = mean_squared_error(label_set['T'], label_set['T_pred'])
      data = data.append({'i' : label, 'mse' : mse}, ignore_index = True)
    return data
    