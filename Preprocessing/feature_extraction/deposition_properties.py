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
    for index,row in data.iterrows():
      if row['d_Q_x']< 3*row['road_width'] and row['d_Q_y']< 3*row['road_width'] and row['d_Q_z']< 3*row['road_width']:
        data['HIZ'].iloc[index] = True
      else:
        data['HIZ'].iloc[index] = False
    data.to_csv('disp_HIZ.csv',encoding='utf-8',  index=False) 
    return data

    
def deposition_properties(data,dp,dm):
    now = datetime.now()
    print('Deposition properties: ' + str(now))
    data = laser_position(data,dp,dm)
    data = laser_d(data)
    data = HIZ(data)
    return data
