# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 12:16:48 2021

@author: kariln
HEAT
"""
import math
from datetime import datetime
from functions import column_check

#PLATE THICKNESS
def beta(data):
    now = datetime.now()
    print('Beta: ' + str(now))
    column_check(data,['I','Q_z','density','cp','v','T_1'])
    data['beta'] = None
    for index,row in data.iterrows():
      if row['I'] == 0:
        data['beta'].iloc[index] = -1
      else:
        data['beta'].iloc[index] = row['Q_z']*math.sqrt(row['density']*row['cp']*row['v']*(row['T_1']-20)/row['I']).real
    data.to_csv('disp_beta.csv',encoding='utf-8',  index=False) 
    return data

#INFLUENCE OF INSTANTANEOUS HEAT SOURCE
def P_inst(data):
    now = datetime.now()
    print('Instantaneous heat source: ' + str(now))
    column_check(data,['I','euclidean_d_Q','density','cp','v', 'diffusivity'])
    data['P_inst'] = None
    for index,row in data.iterrows(): 
      I = row['I']
      rho = row['density']
      cp = row['cp']
      a = row['diffusivity']
      d = row['euclidean_d_Q']
      v = row['v']
      data['P_inst'].iloc[index] = (I/(rho*cp*(4*math.pi*a*d/v)**(3/2))*math.exp(-d*v/(4*a))).real
    data.to_csv('disp_inst.csv',encoding='utf-8',  index=False) 
    return data

#POWER INFLUENCE
def P_inf(data):
    now = datetime.now()
    print('Power influence: ' + str(now))
    column_check(data,['I','euclidean_d_Q','density'])
    data['P_inf'] = None
    for index,row in data.iterrows():
      data['P_inf'].iloc[index] = row['I']/row['euclidean_d_Q'].real
    data.to_csv('disp_Pinf.csv',encoding='utf-8',  index=False) 
    return data

#SURFACE INFLUENZE ZONE
def SIZ(data, seed: float, base_height: float):
    now = datetime.now()
    print('Power influence: ' + str(now))
    column_check(data,['t','road_width','x','y','z'])
    data['SIZ'] = None
    #time_steps = data['t'].unique()
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
      if abs(row['z'] - base_height) < 3*row['road_width']: #checking if the substrate is within the SIZ
        h = row['road_width'] - row['z'] - base_height # height of spherical cap
        r = row['road_width']
        sub_V = math.pi*h**2/3*(3*r-h)
        sub_nodes = sub_V/seed**3
        n_nodes += sub_nodes
      data['SIZ'].iloc[index] = n_nodes/SIZ_nodes_tot
      print('SIZ:'+ str(index))
    data.to_csv('disp_SIZ.csv',encoding='utf-8',  index=False) 
    return data

def heat(data, seed: float, base_height: float):
    now = datetime.now()
    print('Heat: ' + str(now))
    data = beta(data)
    data = P_inst(data)
    data = P_inf(data)
    data = SIZ(data, seed)
    return data
    