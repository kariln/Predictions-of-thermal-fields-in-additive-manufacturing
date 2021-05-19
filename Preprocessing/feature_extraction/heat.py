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
    column_check(data,['I','euclidean_d_Q','v','road_width'])
    data['P_inf'] = None
    for index,row in data.iterrows():
          I = row['I']
          v = row['v']
          d = row['euclidean_d_Q']
          a = row['road_width']
          data['P_inf'].iloc[index] =  I/v*math.exp(-d**2/a**2).real
    data.to_csv('disp_Pinf.csv',encoding='utf-8',  index=False) 
    return data

# def goldak(data):
#     now = datetime.now()
#     print('Goldak: ' + str(now))
#     column_check(data,['Q','road_width','layer_thickness','euclid_grad'])
#     data['goldak'] = None
#     ff = 0.6
#     fr = 1.4
#     af = 0.002
#     ar = 0.004
#     for index,row in data.iterrows():
#           d = row['euclidean_d_Q']
#           b = row['road_width']/2
#           c = row['layer_thickness']
#           Q = row['Q']
#           if row['euclid_grad'] > 0:
#               a = ar
#               f = fr
#           else:
#               a = af
#               f = ff
#           data['goldak'].iloc[index] =  6*math.sqrt(3)*f*Q/(a*b*c*math.pi**(3/2))
#     data.to_csv('disp_goldak.csv',encoding='utf-8',  index=False) 
#     return data

def goldak(data):
    now = datetime.now()
    print('Goldak: ' + str(now))
    column_check(data,['Q','road_width','layer_thickness','euclid_grad'])
    data['P_g'] = None
    ff = 0.6
    fr = 1.4
    af = 0.002
    ar = 0.004
    for index,row in data.iterrows():
          d = row['euclidean_d_Q']
          b = row['road_width']/2
          c = row['layer_thickness']
          Q = row['Q']
          if row['grad_x'] > row['grad_y']:
              x = row['x']-row['Q_x']
              y = row['y']-row['Q_y']
          else:
              y = row['x']-row['Q_x']
              x = row['y']-row['Q_y']
          z = row['z']-row['Q_z']
          if row['euclid_grad'] > 0:
              a = ar
              f = fr
          else:
              a = af
              f = ff
          data['P_g'].iloc[index] =  6*math.sqrt(3)*f*Q/(a*b*c*math.pi**(3/2))*math.exp(-3*(x**2/a**2+y**2/b**2+z**2/c**2)).real
    data.to_csv('disp_goldak.csv',encoding='utf-8',  index=False) 
    return data

def intensity(data):
    now = datetime.now()
    print('Intensity: ' + str(now))
    column_check(data,['Q','A'])
    data['I'] = None
    for index,row in data.iterrows():
      if row['A'] == 0:
        data['I'].iloc[index] = 0
      else:
        data['I'].iloc[index] = row['Q']/row['A']
    data.to_csv('disp_intensity.csv',encoding='utf-8',  index=False) 
    return data
    


def heat(data):
    now = datetime.now()
    print('Heat: ' + str(now))
    data = intensity(data)
    data = P_inf(data)
    #data = goldak(data)
    return data
    