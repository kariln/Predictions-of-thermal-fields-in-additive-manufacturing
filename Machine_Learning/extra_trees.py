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
from feature_extraction.material import material
from feature_extraction.heat import beta,P_inst, P_inf
from feature_extraction.thermal import melt,temp_grad
from dataset import data_frame
import pandas as pd

def extra_trees(nr_estimators: int, train_X, train_Y, test_X, test_Y, metric: str):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    predicted = et_500.predict(test_X)
    train_scores = cross_val_score(et_500, train_X, train_Y, cv=5, scoring=metric)
    test_scores = cross_val_score(et_500, test_X, test_Y, cv=5, scoring=metric)
    return predicted, train_scores, test_scores

def extra_tree_model(nr_estimators: int, train_X, train_Y, test_X, test_Y):
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
    
def node_predict(df_X, model):  
  conductivity = pd.read_csv('AA2319_Conductivity.txt', names=["T","cond"])
  density = pd.read_csv('AA2319_Density.txt', names=["rho"])
  specificHeat = pd.read_csv('AA2319_SpecificHeat.txt', names=["T","cp"])
  #problem med at man sender inn array istedenfor frame - muligens hent columns finn index of ersattt verdi
  predicted = []
  for i, row in df_X.iterrows():
    if i == 0:
      df_X['T_1'].iloc[i]  = 20
      df_X['T_2'].iloc[i]  = 20
      df_X['T_3'].iloc[i]  = 20
      df_X['T_4'].iloc[i]  = 20
      df_X['T_5'].iloc[i]  = 20
      df_X['new'].iloc[i]  = 1
    elif i == 1:
      df_X['T_1'].iloc[i]  = predicted[i-1]
      df_X['T_2'].iloc[i]  = 20
      df_X['T_3'].iloc[i]  = 20
      df_X['T_4'].iloc[i]  = 20
      df_X['T_5'].iloc[i]  = 20
      df_X['new'].iloc[i]  = 2
    elif i == 2:
      df_X['T_1'].iloc[i]  = predicted[i-1]
      df_X['T_2'].iloc[i]  = predicted[i-2]
      df_X['T_3'].iloc[i]  = 20
      df_X['T_4'].iloc[i]  = 20
      df_X['T_5'].iloc[i]  = 20
      df_X['new'].iloc[i]  = 3
    elif i == 3:
      df_X['T_1'].iloc[i]  = predicted[i-1]
      df_X['T_2'].iloc[i]  = predicted[i-2]
      df_X['T_3'].iloc[i]  = predicted[i-3]
      df_X['T_4'].iloc[i]  = 20
      df_X['T_5'].iloc[i]  = 20
      df_X['new'].iloc[i]  = 4
    elif i == 4:
      df_X['T_1'].iloc[i]  = predicted[i-1]
      df_X['T_2'].iloc[i]  = predicted[i-2]
      df_X['T_3'].iloc[i]  = predicted[i-3]
      df_X['T_4'].iloc[i]  = predicted[i-4]
      df_X['T_5'].iloc[i]  = 20
      df_X['new'].iloc[i]  = 5
    else:
      df_X['T_1'].iloc[i]  = predicted[i-1]
      df_X['T_2'].iloc[i]  = predicted[i-2]
      df_X['T_3'].iloc[i]  = predicted[i-3]
      df_X['T_4'].iloc[i]  = predicted[i-4]
      df_X['T_5'].iloc[i]  = predicted[i-5]
      df_X['new'].iloc[i]  = 0
    
    #updating features dependent on T_1
    df_X.iloc[i,:] = material(row.values.reshape(1,-1),density,specificHeat,conductivity)
    df_X.iloc[i,:] = beta(row.values.reshape(1,-1))
    df_X.iloc[i,:] = P_inst(row.values.reshape(1,-1))
    df_X.iloc[i,:] = P_inf(row.values.reshape(1,-1))
    df_X.iloc[i,:] = melt(row.values.reshape(1,-1))
    df_X.iloc[i,:] = temp_grad(row.values.reshape(1,-1))
    
    predict = model.predict(row.values.reshape(1,-1))
    predicted.append(predict[0])
  return df_X,predicted

def test_predict(df_X,model):
    labels = df_X['i'].unique()
    df_X['T_pred'] = None
    for label in labels:
      label_set = df_X[df_X['i'] == label]
      df_X_reset = label_set.reset_index()
      df_X_pred = df_X_reset.drop(columns=['index','T_pred'])
      label_set,predicted = node_predict(df_X_pred,model)
      df_X.shape
      for i,r in label_set.iterrows():
        index = df_X_reset['index'].iloc[i]
        df_X['T_1'].iloc[index] = r['T_1']
        df_X['T_2'].iloc[index] = r['T_2']
        df_X['T_3'].iloc[index] = r['T_3']
        df_X['T_4'].iloc[index] = r['T_4']
        df_X['T_5'].iloc[index] = r['T_5']
        df_X['new'].iloc[index] = r['new']
        df_X['T_pred'].iloc[index] = predicted[i]
    return df_X

def node_predict_plot(predicted,df_Y):
    delta = []
    for i in range(0,len(df_Y.values.tolist())):
      delta.append((df_Y.values.tolist()[i]-predicted[i]))
    
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(9, 9))
    fig.suptitle('Prediction of thermal profile, node 1', fontsize=16)
    ax1.plot(df_X['t'], predicted, label='Predicted', color = 'blue')
    ax1.scatter(df_X['t'], df_Y, label = 'True', color = 'orange')
    ax1.legend()
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature[$C^\circ$]')
    
    ax2.plot(df_X['t'], delta, color = "r", label="Delta = true value - predicted value")
    ax2.set_ylabel('Temperature[$C^\circ$]')
    #par1 = ax2.twinx()
    #par1.plot(df_X['t'], df_X['HIZ'], color = "b", label="Delta", alpha = 0.5)
    ax2.legend()
    
    plt.show()