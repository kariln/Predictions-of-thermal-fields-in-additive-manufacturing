# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:34:36 2021

@author: kariln
"""
import sys
sys.path.append(r'C:\Users\kariln\Documents\GitHub\Master\Machine_Learning')
import pandas as pd
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
from dataset import label_test_split,constant_removal,layer_split,data_split
from extra_trees import extra_tree_model,nodes_predict, feature_importance, permutation_feature_importance,performance,predicted_plot, extra_time
from correlation import correlation_heatmap, highly_correlated_features, shearman_correlation_heatmap,shearman_dendrogram
from sklearn.inspection import plot_partial_dependence
from sklearn.inspection import plot_partial_dependence

filename1 ='preprocessed_1.csv'
data1 = pd.read_csv(filename1, header = 0, sep=',', index_col=False)
# filename2 = 'preprocessed_2.csv'
# data2 = pd.read_csv(filename2, header = 0, sep=',', index_col=False)
# filename3 = 'preprocessed_3.csv'
# data3 = pd.read_csv(filename3, header = 0, sep=',', index_col=False)

# filename4 = 'preprocessed_4.csv'
# data4 = pd.read_csv(filename4, header = 0, sep=',', index_col=False)
filename5 ='preprocessed_5.csv'
data5 = pd.read_csv(filename5, header = 0, sep=',', index_col=False)
# filename6 = 'preprocessed_6.csv'
# data6 = pd.read_csv(filename6, header = 0, sep=',', index_col=False)
# filename7 = 'preprocessed_7.csv'
# data7 = pd.read_csv(filename7, header = 0, sep=',', index_col=False)
# filename8 = 'preprocessed_8.csv'
# data8 = pd.read_csv(filename8, header = 0, sep=',', index_col=False)
# filename9 = 'preprocessed_9.csv'
# data9 = pd.read_csv(filename9, header = 0, sep=',', index_col=False)
# filename10 = 'preprocessed_10.csv'
# data10 = pd.read_csv(filename10, header = 0, sep=',', index_col=False)
# filename11 = 'preprocessed_11.csv'
# data11 = pd.read_csv(filename11, header = 0, sep=',', index_col=False)
# filename12 = 'preprocessed_12.csv'
# data12 = pd.read_csv(filename12, header = 0, sep=',', index_col=False)


data1 = data1.drop(columns = ['i',"T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','grad_x','grad_y','grad_z', 'Q', 'd_top', 'd_bottom', 'd_x1', 'd_x2', 'd_y1','d_y2', 'category', 'I', 'road_width', 'dT_12', 'dT_23', 'dT_34', 'dT_45','density', 'specificheat', 'conductivity', 'E','diffusivity', 'melt', 'beta', 'v', 'P_inst', 'A', 'layer_thickness', 'basedepth','layerNum','d_Q_x','d_Q_y','d_Q_z','dt_i','P_g','laser_dir','manh_d_Q','HIZ','Q_tot','euclid_grad'])
#data2 = data2.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','grad_x','grad_y','grad_z', 'Q', 'd_top', 'd_bottom', 'd_x1', 'd_x2', 'd_y1','d_y2', 'category', 'I', 'road_width', 'dT_12', 'dT_23', 'dT_34', 'dT_45', 'v', 'A', 'layer_thickness', 'basedepth','pattern','P_density','i','layerNum','d_Q_x','d_Q_y','d_Q_z','dt_i','P_g','laser_dir','manh_d_Q','HIZ','Q_tot','euclid_grad'])
#data4 = data4.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','i','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','pattern','globalseed','surface','nr_surf_nodes','Q_tot','manh_d_Q','euclid_grad','laser_dir','grad_x','grad_y','grad_z','P_g'])
data5 = data5.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','grad_x','grad_y','grad_z', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','pattern','euclid_grad','globalseed','d_Q_x','d_Q_y','d_Q_z','layerNum','manh_d_Q','P_g','HIZ','laser_dir','Q_tot','i','surface','nr_surf_nodes','dt_i'])
#data6 = data6.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','i','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','pattern','Q_tot','globalseed'])
#data7 = data7.drop(columns = ['i',"T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','grad_x','grad_y','grad_z', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','pattern','euclid_grad','globalseed','d_Q_x','d_Q_y','d_Q_z','layerNum','manh_d_Q','P_g','HIZ','laser_dir','Q_tot'])
#data8 = data8.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y','Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','i','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','pattern','globalseed','Q_tot','i'])
#data9 = data9.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','pattern','euclid_grad','globalseed','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','laser_dir','Q_tot','i'])
#data10 = data10.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','pattern','globalseed','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','Q_tot'])
#data11 = data11.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','Q_tot','i'])
#data12 = data12.drop(columns = ["T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','Q_tot','i'])
#data3 = data3.drop(columns = ['globalseed','euclid_grad','laser_dir','pattern',"T_1","T_2","T_3","T_4","T_5",'x','y','z','Q_z','Q_x','Q_y', 'Q', 'I', 'road_width', 'v', 'A', 'layer_thickness', 'basedepth','d_Q_x','d_Q_y','d_Q_z','layerNum','HIZ','Q_tot','i'])


# data_7_10 = data10[data10['i'] == 34]
# data7 = data10[data10['i'] != 34]
# data7 = data10.drop(columns = ['i'])
# data_7_10 = data_7_10.drop(columns = ['i'])

# data_1_10 = data1[data1['i'] == 10]
# data1 = data1[data1['i'] != 10]
# data1 = data1.drop(columns = ['i'])
# data_1_10 = data_1_10.drop(columns = ['i'])

data = data1.append(data5)
#data = data.append(data)
#data = data.rename(columns = {'euclidean_d_Q':'d_e'}, inplace = False)
X_11 = data.drop(columns = ['T'])
Y_11 = data['T']

# X_1 = data7.drop(columns = ['T'])
# Y_1 = data7['T']

#X,Y,train_X, test_X, train_Y, test_Y= data_split(data)

et_500 = extra_tree_model(55, X_11, Y_11)
sns.set(font_scale=1)

features = [4]
plot_partial_dependence(et_500, X_11, features) 


# predicted = et_500.predict(test_X)
# data_p = performance(test_X,test_Y,predicted)
# print(data_p)
#predicted_plot(predicted,Y_1)
# train_scores = cross_val_score(et_500, X_11, Y_11, cv=2, scoring='neg_mean_absolute_error')
# print(sum(train_scores)/2)


# pred = et_500.predict(data_7_10.drop(columns=['T']))

# sns.set(font_scale=1)
# delta = []
# for i in range(0,len(data_7_10['T'].values.tolist())):
#   delta.append(data_7_10['T'].values.tolist()[i]-pred[i])

# fig, (ax1,ax2) = plt.subplots(2,1,figsize=(9, 9))
# fig.suptitle('Prediction of thermal profile, node 10', fontsize=16)
# ax1.plot(data_7_10['t'],pred, label='Predicted', color = 'blue')
# ax1.scatter(data_7_10['t'],data_7_10['T'], label = 'True', color = 'orange')
# #ax1.axvline(x=test_X['t'].iloc[0], color = 'firebrick',linestyle='dashed', label = 'Dataset limit')
# ax1.legend()
# ax1.set_xlabel('Time [s]')
# ax1.set_ylabel('Temperature[$C^\circ$]')

# ax2.plot(data_7_10['t'], delta, color = "r", label="$r_t = y_i - \hat{y}_i$")
# ax2.set_ylabel('Temperature[$C^\circ$]')
# ax2.legend()
# plt.show()


#data = data1.append(data2)
#data = data.append(data7)

#data = data.rename(columns = {'euclidean_d_Q': 'd_e', 'manh_d_Q': 'd_m', 'euclid_grad' : 'dd_e', 'laser_dir':'l_dir'}, inplace = False)


# X,Y,train_X, test_X, train_Y, test_Y =  data_split(data)
# et_500 = extra_tree_model(2, train_X, train_Y)
# # # predicted = et_500.predict(test_X)
# # # data_p = performance(test_X,test_Y,predicted)
# # # print(data_p)
# # # train_scores = cross_val_score(et_500, train_X, train_Y, cv=5, scoring='neg_mean_absolute_error')
# # # print(train_scores)
# sns.set(font_scale=2)
# #permutation_feature_importance(et_500, test_X, test_Y)
# # #predicted_plot(predicted,test_Y)
# # sns.set(font_scale=2)
# features = [1]
# plot_partial_dependence(et_500, X, features, percentiles=(0, 1)) 
