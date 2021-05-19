# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:33:54 2021

@author: kariln

SPATIAL FEATURES
"""
from scipy.spatial import distance
from datetime import datetime
from functions import column_check
import numpy as np

def euclidean(data):
    now = datetime.now()
    print('Euclidean: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z'])
    data['euclidean_d_Q'] = None
    for index, row in data.iterrows():
      a = (row['Q_x'], row['Q_y'], row['Q_z'])
      b = (row['x'], row['y'], row['z'])
      dst = distance.euclidean(a, b)
      data['euclidean_d_Q'].iloc[index] = dst
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def manhattan(data):
    now = datetime.now()
    print('Manhattan: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z'])
    data['manh_d_Q'] = None
    for index, row in data.iterrows():
      a = (row['Q_x'], row['Q_y'], row['Q_z'])
      b = (row['x'], row['y'], row['z'])
      dst = distance.cityblock(a, b)
      data['manh_d_Q'].iloc[index] = dst
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def laser_distance(data):
    now = datetime.now()
    print('Laser distance: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z','road_width','layer_thickness'])
    data['d_Q_x'] = None
    data['d_Q_y'] = None
    data['d_Q_z'] = None
    for index, row in data.iterrows():
      data['d_Q_x'].iloc[index] = abs(row['Q_x']-row['x'])/row['road_width']
      data['d_Q_y'].iloc[index] = abs(row['Q_y']-row['y'])/row['road_width']
      data['d_Q_z'].iloc[index] = abs(row['Q_z']-row['z'])/row['layer_thickness']
    data.to_csv('disp_d_Q.csv',encoding='utf-8',  index=False) 
    return data

def euclid_grad(data):
    now = datetime.now()
    print('Euclidean gradient: ' + str(now))
    column_check(data,['euclidean_d_Q'])
    data['euclid_grad'] = None
    num_i = data['i'].nunique()
    i = data['i'].unique()
    for j in range(0,num_i):
      data_i = data[data['i'] == i[j]] 
      indexes = data_i.index
      num = 0
      for index,row in data_i.iterrows():
        if num == 0: 
          data['euclid_grad'].iloc[index] = 0
        else:
          data['euclid_grad'].iloc[index] = data['euclidean_d_Q'].iloc[indexes[num]]-data['euclidean_d_Q'].iloc[indexes[num-1]]
        num += 1
    data.to_csv('disp_grad.csv',encoding='utf-8',  index=False) 
    return data

def dist_grad(data):
    now = datetime.now()
    print('Distance gradient: ' + str(now))
    column_check(data,['euclidean_d_Q'])
    data['grad_x'] = None
    data['grad_y'] = None
    data['grad_z'] = None
    num_i = data['i'].nunique()
    i = data['i'].unique()
    for j in range(0,num_i):
      data_i = data[data['i'] == i[j]] 
      indexes = data_i.index
      num = 0
      for index,row in data_i.iterrows():
        if num == 0: 
          data['grad_x'].iloc[index] = 0
          data['grad_y'].iloc[index] = 0
          data['grad_z'].iloc[index] = 0
        else:
          data['grad_x'].iloc[index] = abs(data['d_Q_x'].iloc[indexes[num]]-data['d_Q_x'].iloc[indexes[num-1]])
          data['grad_y'].iloc[index] = abs(data['d_Q_y'].iloc[indexes[num]]-data['d_Q_y'].iloc[indexes[num-1]])
          data['grad_z'].iloc[index] = abs(data['d_Q_z'].iloc[indexes[num]]-data['d_Q_z'].iloc[indexes[num-1]])
        num += 1
    data.to_csv('disp_graddist.csv',encoding='utf-8',  index=False) 
    return data

def laser_dir(data):
    now = datetime.now()
    print('Laser direction: ' + str(now))
    column_check(data,['euclid_grad'])
    data['laser_dir'] = None
    for index,row in data.iterrows():
      if row['euclid_grad'] > 0: 
        data['laser_dir'].iloc[index] = 1
      else:
        data['laser_dir'].iloc[index] = 0
    data.to_csv('disp_dir.csv',encoding='utf-8',  index=False) 
    return data

def layerNum(data, nr_layers: int):
    now = datetime.now()
    print('Layer number: ' + str(now))
    column_check(data,['z','layer_thickness','basedepth'])
    data['layerNum'] = None
    layer_thickness = data['layer_thickness'].iloc[0]
    base_height = data['basedepth'].iloc[0]
    
    #Finding layer numbers and heights
    layer_num = data['z'].nunique()
    layers = np.linspace(0, layer_num, layer_num, endpoint=False)
    heights = data['z'].unique()
    for index,row in data.iterrows():
        i = 0
        for height in heights:
            if height == row['z']:
                data['layerNum'].iloc[index] = layers[i]
                break
            i += 1
    data.to_csv('disp_layer.csv',encoding='utf-8',  index=False) 
    return data

def neighbor(data):
    now = datetime.now()
    print('Neighbor: ' + str(now))
    data['t_n'] = None
    data['t_HIZ'] = None
    column_check(data,['t','x','y','z','road_width','d_Q_x','d_Q_y','d_Q_z','HIZ'])
    i_unique = data[['i', 'x','y','z','road_width','t_n','t_HIZ']]
    i_unique = i_unique.drop_duplicates()
    i_unique = i_unique.reset_index()
    i_unique['t_n']= 0
    i_unique['t_n']= 0
    a = data['road_width'].iloc[0]
    for j,row in data.iterrows():
        print('index: ' + str(index))
        if row['d_Q_x'] < 1 or row['d_Q_y'] < 1 or row['d_Q_z'] < 1:
            for i,r in i_unique.iterrows():
                if row['i'] == r['i']:
                    i_unique['t_n'].iloc[i] = 0
            data['t_n'].iloc[index] = 0
            data['t_HIZ'].iloc[index] = 0
        elif row['HIZ'] == 1:
            data['t_HIZ'].iloc[index] = 0
        else:
            for i,r in i_unique.iterrows():
                if row['i'] == r['i']:
                    data['VR'].iloc[index] = r['VR']
    data.to_csv('disp_SIZ_V.csv',encoding='utf-8',  index=False) 
    return data



def spatial(data, nr_layers: int):
    now = datetime.now()
    print('Spatial: ' + str(now))
    data = layerNum(data, nr_layers)
    data = euclidean(data)
    #data = manhattan(data)
    data = euclid_grad(data)
    data = laser_dir(data)
    #data = laser_distance(data)
    #data =  dist_grad(data)
    return data
