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
from metrics import results
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import seaborn as sns

def extra_trees(nr_estimators: int, train_X, train_Y, test_X, test_Y, metric: str):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    predicted = et_500.predict(test_X)
    train_scores = cross_val_score(et_500, train_X, train_Y, cv=5, scoring=metric)
    return predicted, train_scores

def extra_tree_model(nr_estimators: int, train_X, train_Y):
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    et_500.fit(train_X,train_Y)
    return et_500

def extra_time(nr_estimators:int,train_X,train_Y,test_X):
    t_unique = test_X['t'].unique()
    temp_X = train_X
    temp_Y = train_Y
    et_500 = ExtraTreesRegressor(n_estimators=nr_estimators, n_jobs=-1, random_state=300)
    predicted = []
    for t in t_unique:
        et_500.fit(temp_X,temp_Y)
        tmp_X = test_X[test_X['t'] == t]
        test_X = test_X[test_X['t'] != t]
        pred = et_500.predict(tmp_X)
        pred = pd.DataFrame(pred, columns = ['T'])
        for index,row in pred.iterrows():
            predicted.append(row['T'])
        temp_X.append(tmp_X)
        temp_Y.append(pred)
    return predicted,temp_Y,et_500

def feature_importance(model, train_X):
    nr_features = train_X.shape[1]
    skplt.estimators.plot_feature_importances(model,text_fontsize=16,max_num_features=nr_features,figsize=(30,4),feature_names=train_X.columns)
    plt.xticks(rotation=90, fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.title('Feature importance', fontsize = 30)
    plt.savefig('feature_importance', bbox_inches = "tight")
    plt.savefig('feature_imp.png')
    plt.show()

def permutation_feature_importance(model, test_X,test_Y):
    fig = plt.figure(figsize=(18,9))
    sorted_idx = model.feature_importances_.argsort()
    perm_importance = permutation_importance(model, test_X, test_Y)
    sorted_idx = perm_importance.importances_mean.argsort()
    plt.barh(test_X.columns[sorted_idx], perm_importance.importances_mean[sorted_idx])
    plt.xlabel("Permutation Importance")
    plt.savefig('permutation', bbox_inches = "tight")
    plt.show()

def test_predict(df_X,model):
    labels = df_X['i'].unique()
    df_X['T_pred'] = -99
    for label in labels:
      label_set = df_X[df_X['i'] == label]
      df_X_reset = label_set.reset_index()
      df_X_pred = df_X_reset.drop(columns=['index','T_pred'])
      predicted = model.predict(df_X.drop(columns=['T_pred','i']))
      for i,r in df_X_pred.iterrows():
        index = df_X_reset['index'].iloc[i]
        df_X['T_pred'].iloc[index] = predicted[i]
    return df_X
    
def node_predict_plot(df):
    sns.set(font_scale=2)
    column_check(df,['T_pred'])
    delta = []
    label = df['i'].iloc[0]
    for i in range(0,len(df.values.tolist())):
      delta.append((df['T'].values.tolist()[i]-df['T_pred'].values.tolist()[i]))
    
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(9, 12))
    #fig.suptitle('Prediction of thermal profile, node' + str(label))
    ax1.plot(df['t'], df['T_pred'], label='Predicted', color = 'blue')
    ax1.scatter(df['t'], df['T'], label = 'True', color = 'orange')
    ax1.legend()
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature[$C^\circ$]')
    
    ax2.plot(df['t'], delta, color = "r", label="$r_t = y_i - \hat{y}_i$")
    ax2.set_ylabel('Temperature[$C^\circ$]')
    ax2.legend()
    plt.savefig('node_{:d}'.format(label), bbox_inches = "tight")
    plt.show()
    
def nodes_plot(df_Y,df_X):#virker ikke på flere nodes
    column_check(df_X,['T_pred'])
    df_X['T'] = df_Y['T']
    labels = df_X['i'].unique()
    for label in labels:
        label_set = df_X[df_X['i'] == label]
        predicted = label_set['T_pred']
        true = label_set['T']
        node_predict_plot(predicted,true,label_set)
        
        plt.savefig('node_{:d}'.format(label), bbox_inches = "tight")
        
def predicted_plot(predicted,true):
    sns.set(font_scale=2.5)
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 10))
    sns.color_palette()
    plt.scatter(predicted,true, label = 'Predicted samples', color = 'tab:blue')
    xpoints = ypoints = plt.gca().get_xlim()
    plt.plot(xpoints, ypoints, lw=3, color = 'black', linestyle='dashed',scalex=False,scaley=False, label = 'Perfect prediction')
    plt.title('Predicted versus true values')
    plt.xlabel('Predicted values')
    plt.ylabel('True values')
    plt.legend()

def nodes_predict(df,model):
    labels = df['i'].unique()
    df_X = df.drop(columns=['T'])
    for label in labels:
        label_set = df_X[df_X['i'] == label]
        label_set_tot = df[df['i'] == label].reset_index()
        predicted = model.predict(label_set.drop(columns=['i']))
        i=0
        label_set['T_pred'] = -99
        label_set_reset = label_set.reset_index()
        for index,row in label_set_reset.iterrows():
            label_set_reset['T_pred'].iloc[index] = predicted[i]
            i += 1
        label_set_tot['T_pred'] = label_set_reset['T_pred']
        performance =  node_performance(label_set_tot)
        node_predict_plot(label_set_tot)
    
def node_performance(df):
    column_check(df,['T_pred'])
    label = df['i'].iloc[0]
    data = pd.DataFrame(columns=['i','R2','R2_adjust','MAE','MAPE','MSE','NMSE','RMSE','NRMSE'])
    test_X = df.drop(columns=['T_pred','T'])
    y_pred = df['T_pred']
    y_true = df['T']
    R2, R2_adjust,MAE,MAPE,MSE,NMSE,RMSE,NRMSE = results(y_true,y_pred, test_X)
    data = data.append({'i' : label,'R2' : R2,'R2_adjust' : R2_adjust,'MAE' : MAE,'MAPE' : MAPE,'MSE' : MSE,'NMSE' : NMSE,'RMSE' : RMSE,'NRMSE' : NRMSE}, ignore_index = True)
    return data

def performance(test_X,test_Y,predicted):
    data = pd.DataFrame(columns=['R2','R2_adjust','MAE','MAPE','MSE','NMSE','RMSE','NRMSE'])
    y_pred = predicted
    y_true = test_Y
    R2, R2_adjust,MAE,MAPE,MSE,NMSE,RMSE,NRMSE = results(y_true,y_pred, test_X)
    data = data.append({'R2' : R2,'R2_adjust' : R2_adjust,'MAE' : MAE,'MAPE' : MAPE,'MSE' : MSE,'NMSE' : NMSE,'RMSE' : RMSE,'NRMSE' : NRMSE}, ignore_index = True)
    return data

def grid_search_tree_size(data):
    sns.color_palette("Paired")
    sns.set(font_scale=4)
    Y_col = ['T']
    X = data.drop(Y_col, axis=1) #Input dataframe, X
    Y = pd.DataFrame(data, columns=Y_col) #Output dataframe, Y

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, 
                                                    train_size=0.8,
                                                    test_size=0.2,
                                                    random_state=42)
    # grid search
    et_500 = ExtraTreesRegressor()
    n_estimators = range(5,110,10)
    param_grid = dict(n_estimators=n_estimators)
    grid_search = GridSearchCV(et_500, param_grid, scoring="r2", n_jobs=-1, cv=5)
    grid_result = grid_search.fit(train_X, train_Y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    fit_time = grid_result.cv_results_['mean_fit_time']
    score_time = grid_result.cv_results_['mean_score_time']
    for mean, stdev, param, f_t,s_t in zip(means, stds, params, fit_time,score_time):
        print("%f (%f) with: %r, fit time: %f, score time: %f" % (mean, stdev, param,f_t,s_t))
        # plot accuracy
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    plt.errorbar(n_estimators, means, color = 'tab:blue')
    plt.title("Grid search of nr. of trees in forrest")
    plt.xlabel('Number of trees')
    plt.ylabel('R2')
    plt.savefig('n_estimators.png')

    # plot time
    fig, host = plt.subplots(1, 1, figsize=(20, 10))
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()

    p1, = host.plot(n_estimators, fit_time, "b-", label="Fit time")
    p2, = par1.plot(n_estimators, score_time, "orange", label="Score time")
    
    host.title('Time consumption based on number of trees')
    host.set_xlabel('Number of trees')
    host.set_ylabel("Fit time")
    par1.set_ylabel("Score time")

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)


    lines = [p1, p2]

    host.legend(lines, [l.get_label() for l in lines])
    host.savefig('time.png')
    plt.show()
    return means, fit_time, score_time
 
    
# def node_predict(df_X_pred, model):  
#   conductivity = pd.read_csv('AA2319_Conductivity.txt', names=["T","K"])
#   specificHeat = pd.read_csv('AA2319_SpecificHeat.txt', names=["T","cp"])
#   density = pd.read_csv('AA2319_Density.txt', names=["rho"])
#   #problem med at man sender inn array istedenfor frame - muligens hent columns finn index of ersattt verdi
#   predicted = []

#   for i, row in df_X_pred.iterrows():
#     if i == 0:
#       row['T_1']  = 20
#       row['T_2']  = 20
#       row['T_3']  = 20
#       row['T_4']  = 20
#       row['T_5']  = 20
#       row['new']  = 1
#     elif i == 1:
#       row['T_1']  = predicted[i-1]
#       row['T_2']  = 20
#       row['T_3']  = 20
#       row['T_4']  = 20
#       row['T_5']  = 20
#       row['new']  = 2
#     elif i == 2:
#       row['T_1']  = predicted[i-1]
#       row['T_2']  = predicted[i-2]
#       row['T_3']  = 20
#       row['T_4']  = 20
#       row['T_5']  = 20
#       row['new']  = 3
#     elif i == 3:
#       row['T_1']  = predicted[i-1]
#       row['T_2']  = predicted[i-2]
#       row['T_3']  = predicted[i-3]
#       row['T_4']  = 20
#       row['T_5']  = 20
#       row['new']  = 4
#     elif i == 4:
#       row['T_1']  = predicted[i-1]
#       row['T_2']  = predicted[i-2]
#       row['T_3']  = predicted[i-3]
#       row['T_4']  = predicted[i-4]
#       row['T_5']  = 20
#       row['new']  = 5
#     else:
#       row['T_1']  = predicted[i-1]
#       row['T_2']  = predicted[i-2]
#       row['T_3']  = predicted[i-3]
#       row['T_4']  = predicted[i-4]
#       row['T_5']  = predicted[i-5]
#       row['new']  = 0
    
#     #updating features dependent on T_1
#     sub_dataframe = df_X_pred.iloc[[i], :]
#     sub_dataframe = sub_dataframe.reset_index()
#     sub_dataframe = sub_dataframe.drop(columns=['index'])
    
#     #Material
#     sub_dataframe = material(sub_dataframe,density,specificHeat,conductivity).iloc[[0], :]
#     df_X_pred['density'].iloc[i] = sub_dataframe['density'].iloc[0]
#     df_X_pred['K'].iloc[i] = sub_dataframe['K'].iloc[0]
#     df_X_pred['cp'].iloc[i] = sub_dataframe['cp'].iloc[0]
#     df_X_pred['diffusivity'].iloc[i] = sub_dataframe['diffusivity'].iloc[0]
    
#     #Heat
#     sub_dataframe = beta(sub_dataframe).iloc[[0], :]
#     df_X_pred['beta'].iloc[i] = sub_dataframe['beta'].iloc[0]
    
#     sub_dataframe = P_inst(sub_dataframe).iloc[[0], :]
#     df_X_pred['P_inst'].iloc[i] = sub_dataframe['P_inst'].iloc[0]
    
#     sub_dataframe = melt(sub_dataframe).iloc[[0], :]
#     df_X_pred['melt'].iloc[i] = sub_dataframe['melt'].iloc[0]
    
#     sub_dataframe = temp_grad(sub_dataframe).iloc[[0], :]
#     df_X_pred['dT_12'].iloc[i] = sub_dataframe['dT_12'].iloc[0]
#     df_X_pred['dT_23'].iloc[i] = sub_dataframe['dT_23'].iloc[0]
#     df_X_pred['dT_34'].iloc[i] = sub_dataframe['dT_34'].iloc[0]
#     df_X_pred['dT_45'].iloc[i] = sub_dataframe['dT_45'].iloc[0]

#     predict = model.predict(row.values.reshape(1,-1))
#     predicted.append(predict[0])
#   return df_X_pred,predicted

# def test_predict(df_X,model):
#     labels = df_X['i'].unique()
#     df_X['T_pred'] = -99
#     df_X['density'] = -99
#     df_X['cp'] = -99
#     df_X['K'] = -99
#     df_X['diffusivity'] = -99
#     df_X['beta'] = -99
#     df_X['P_inst'] = -99
#     df_X['melt'] = -99
#     df_X['dT_12'] = -99
#     df_X['dT_23'] = -99
#     df_X['dT_34'] = -99
#     df_X['dT_45'] = -99
#     for label in labels:
#       label_set = df_X[df_X['i'] == label]
#       df_X_reset = label_set.reset_index()
#       df_X_pred = df_X_reset.drop(columns=['index','T_pred'])
#       df_X_pred,predicted = node_predict(df_X_pred,model)
#       for i,r in df_X_pred.iterrows():
#         index = df_X_reset['index'].iloc[i]
#         df_X['T_1'].iloc[index] = r['T_1']
#         print(df_X['T_1'].iloc[index] - r['T_1'])
#         df_X['T_2'].iloc[index] = r['T_2']
#         df_X['T_3'].iloc[index] = r['T_3']
#         df_X['T_4'].iloc[index] = r['T_4']
#         df_X['T_5'].iloc[index] = r['T_5']
#         df_X['new'].iloc[index] = r['new']
#         df_X['density'].iloc[index] = r['density']
#         df_X['K'].iloc[index] = r['K']
#         df_X['cp'].iloc[index] = r['cp']
#         df_X['diffusivity'].iloc[index] = r['diffusivity']
#         df_X['beta'].iloc[index]=r['beta']
#         df_X['P_inst'].iloc[index] = r['P_inst']
#         df_X['melt'].iloc[index] = r['melt']
#         df_X['dT_12'].iloc[index] = r['dT_12']
#         df_X['dT_23'].iloc[index] = r['dT_23']
#         df_X['dT_34'].iloc[index] = r['dT_34']
#         df_X['dT_45'].iloc[index]=r['dT_45']
#         df_X['T_pred'].iloc[index] = predicted[i]
#     return df_X