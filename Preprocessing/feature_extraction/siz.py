# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:36:32 2021

@author: kariln
"""

import pandas as pd
import math

data = pd.read_csv(r'C:\Master\disp_euclid (4).csv', header = 0, sep=',', index_col=False)
#SURFACE INFLUENZE ZONE
data['SIZ'] = None
seed = 0.0023 #Approximate global size of seeds
data['sub_z'] = 0.005 #z-coordinate of the substrate
time_steps = data['t'].unique()
SIZ_V = 4/3*math.pi*data['road_width'].iloc[0]**3
SIZ_nodes_tot = SIZ_V/seed**3
for index,row in data.iterrows(): 
  data_time = data[data['t'] == row['t']]
  n_nodes = 0
  for i,r in data_time.iterrows(): 
    dx = abs(row['x']-r['x'])
    dy = abs(row['y']-r['y'])
    dz = abs(row['z']-r['z'])
    if dx< 3*row['road_width'] and dy< 3*row['road_width'] and dz< 3*row['road_width']:
      n_nodes += 1
    else:
      pass
  if abs(row['z'] - row['sub_z']) < 3*row['road_width']: #checking if the substrate is within the SIZ
    h = row['road_width'] - row['z'] - row['sub_z'] # height of spherical cap
    r = row['road_width']
    sub_V = math.pi*h**2/3*(3*r-h)
    sub_nodes = sub_V/seed**3
    n_nodes += sub_nodes
  data['SIZ'].iloc[index] = n_nodes/SIZ_nodes_tot
  print(index)
data.to_csv('disp_SIZ.csv',encoding='utf-8',  index=False) 
