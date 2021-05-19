# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:06:13 2021

@author: kariln

DEPOSITION PROPERTIES
data: dataset
dm: material path
dp: heat path
"""
from functions import interpolate, column_check 
from datetime import datetime
import pandas as pd
import numpy as np
import math

def laser_position(data, dp,dm):
    now = datetime.now()
    print('Laser position: ' + str(now))
    column_check(data,['t','x','y','z'])
    data['Q'] = None
    data['Q_x'] = None
    data['Q_y'] = None
    data['Q_z'] = None 
    data['A'] = None
    data['Q_tot'] = None
    time = 0
    Q = None
    Q_x = None
    Q_y = None
    Q_z = None
    Q_tot = 0
    dp['A'] = dm['A']
    index = 0
    for j,row in data.iterrows():
      time = row['t']
      for i,r in dp.iterrows():
        if float(time) < float(r['t']) and i != 0:
          prev_r = dp.loc[ i-1 , : ]
          Q_x = interpolate(prev_r['t'],r['t'],prev_r['x'],r['x'],time)
          Q_y = interpolate(prev_r['t'],r['t'],prev_r['y'],r['y'],time)
          Q_z = interpolate(prev_r['t'],r['t'],prev_r['z'],r['z'],time)
          Q = prev_r['Q']
          A = prev_r['A']
          Q_tot += prev_r['Q']*(r['t']-prev_r['t'])
          break
        elif float(time) < float(r['t']) and i == 0:
          Q_x = r['x']
          Q_y = r['y']
          Q_z = r['z']
          Q = r['Q']
          A = r['A']
          break
        else:
          continue
      print(index)
      data['Q'].iloc[index] = Q
      data['Q_x'].iloc[index] = Q_x
      data['Q_y'].iloc[index] = Q_y
      data['Q_z'].iloc[index] = Q_z  
      data['A'].iloc[index] = A
      data['Q_tot'].iloc[index] = Q_tot
      index +=1
    data.to_csv('disp_laser_pos.csv',encoding='utf-8',  index=False) 
    return data

def laser_d(data):
    now = datetime.now()
    print('Laser distance: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z'])
    data['d_Q_x'] = abs(data['Q_x']-data['x'])
    data['d_Q_y'] = abs(data['Q_y']-data['y'])
    data['d_Q_z'] = abs(data['Q_z']-data['z'])
    data.to_csv('disp_laser_d.csv',encoding='utf-8',  index=False) 
    return data

def bead_area(data,dm):
    now = datetime.now()
    print('Bead area: ' + str(now))
    column_check(data,['t'])
    data['A'] = None
    time = 0
    A = None
    for index,row in data.iterrows():
      time = row['t']
      for i,r in dm.iterrows():
        if float(time) < float(r['t']) and i != 0:
          prev_r = dm.loc[ i-1 , : ]
          A = prev_r['A']
          break
        elif float(time) < float(r['t']) and i == 0:
          A = r['A']
          break
        else:
          continue
      data['A'].iloc[index] = A
    data.to_csv('disp_bead.csv',encoding='utf-8',  index=False) 
    return data

def velocity(data, v: float):
    now = datetime.now()
    print('Velocity: ' + str(now))
    data['v'] = v
    data.to_csv('disp_v.csv',encoding='utf-8',  index=False) 
    return data

def roadWidth(data, road_width: float):
    now = datetime.now()
    print('Road width: ' + str(now))
    data['road_width'] = road_width
    data.to_csv('disp_road.csv',encoding='utf-8',  index=False) 
    return data

def intensity(data):
    now = datetime.now()
    print('Intensity: ' + str(now))
    column_check(data,['A','Q'])
    data['I'] = None
    for index,row in data.iterrows():
        if row['A'] == 0:
            data['I'].iloc[index] = 0
        else:
            data['I'].iloc[index] = abs(row['Q']/row['A'])
    data.to_csv('disp_I.csv',encoding='utf-8',  index=False) 
    return data


def P_density(data):
    now = datetime.now()
    print('Power density: ' + str(now))
    column_check(data,['A','Q','v'])
    data['P_density'] = None
    for index,row in data.iterrows():
        if row['A'] == 0:
            data['P_density'].iloc[index] = 0
        else:
            data['P_density'].iloc[index] = row['Q']/(row['v']*row['A'])
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def HIZ(data):
    now = datetime.now()
    print('HIZ: ' + str(now))
    column_check(data,['d_Q_x','d_Q_y','d_Q_z','road_width'])
    data['HIZ'] = None
    a = data['road_width'].iloc[-1] 
    for index,row in data.iterrows():
      if row['d_Q_x']<= 3*a and row['d_Q_y']<= 3*a and row['d_Q_z']<= 3*a:
        data['HIZ'].iloc[index] = True
      else:
        data['HIZ'].iloc[index] = False
    data.to_csv('disp_HIZ.csv',encoding='utf-8',  index=False) 
    return data

def neighbor(data):
    now = datetime.now()
    print('Neighbor: ' + str(now))
    column_check(data,['d_Q_x','d_Q_y','d_Q_z','road_width'])
    data['n'] = None
    a = data['road_width'].iloc[-1] 
    for index,row in data.iterrows():
      if row['d_Q_x']<= 1*a and row['d_Q_y']<= 1*a and row['d_Q_z']<= 1*a:
        data['n'].iloc[index] = True
      else:
        data['n'].iloc[index] = False
    data.to_csv('disp_neighbor.csv',encoding='utf-8',  index=False) 
    return data

def neighbor_time(data):
    now = datetime.now()
    print('Neighbor time: ' + str(now))
    data['t_n'] = None
    data['t_HIZ'] = None
    column_check(data,['t','x','y','z','road_width','HIZ','n', 'road_width','v'])
    i_unique = data[['i', 't_n','t_HIZ']]
    i_unique = i_unique.drop_duplicates()
    i_unique = i_unique.reset_index()
    i_unique['t_n']= 0
    i_unique['t_HIZ']= 0
    a = data['road_width'].iloc[0]
    t = 0
    prev_t = 0
    for index,row in data.iterrows():
        print('index: ' + str(index))
        v = data['v'].iloc[index]
        if row['t'] > t:
            prev_t = t
            t = row['t']
        if row['n'] == True:
            for i,r in i_unique.iterrows():
                if row['i'] == r['i']:
                    i_unique['t_n'].iloc[i] = 0
                    i_unique['t_HIZ'].iloc[i] = 0
                    break
            data['t_n'].iloc[index] = 0
            data['t_HIZ'].iloc[index] = 0
        elif row['HIZ'] == True:
            for i,r in i_unique.iterrows():
                if row['i'] == r['i']:
                    i_unique['t_n'].iloc[i] += (t-prev_t)*v
                    data['t_n'].iloc[index] = r['t_n']
                    i_unique['t_HIZ'].iloc[i] = 0
                    break
            data['t_HIZ'].iloc[index] = 0
        else:
            for i,r in i_unique.iterrows():
                if row['i'] == r['i']:
                    i_unique['t_n'].iloc[i] += (t-prev_t)*v
                    data['t_n'].iloc[index] = r['t_n']
                    i_unique['t_HIZ'].iloc[i] += (t-prev_t)*v
                    data['t_HIZ'].iloc[index] = r['t_HIZ']
                    break
    data.to_csv('disp_neighbor_time.csv',encoding='utf-8',  index=False) 
    return data

def weighted_time(data):
    now = datetime.now()
    print('Weighted time: ' + str(now))
    column_check(data,['I','euclidean_d_Q','v','road_width','t_n','t_HIZ'])
    data['t_n_w'] = None
    data['t_HIZ_w'] = None
    for index,row in data.iterrows():
          I = row['I']
          t_n = row['t_n']
          t_HIZ = row['t_HIZ']
          data['t_n_w'].iloc[index] =  I*math.exp(t_n).real
          data['t_HIZ_w'].iloc[index] =  I*math.exp(t_HIZ).real
    data.to_csv('disp_weighted_time.csv',encoding='utf-8',  index=False) 
    return data

def init_time(data):
    now = datetime.now()
    print('Initialization time: ' + str(now))
    column_check(data,['t','t_i'])
    data['dt_i'] = None
    for index,row in data.iterrows():
          data['dt_i'].iloc[index] =  (row['t']-row['t_i'])/row['t']
    data.to_csv('disp_init_time.csv',encoding='utf-8',  index=False) 
    return data

def deposition_properties(data,dp,dm):
    now = datetime.now()
    print('Deposition properties: ' + str(now))
    data = laser_position(data,dp,dm)
    data = laser_d(data)
    #data = HIZ(data)
    data = neighbor(data)
    data = neighbor_time(data)
    #data = weighted_time(data)
    #data = init_time(data)
    return data
