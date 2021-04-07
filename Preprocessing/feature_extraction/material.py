# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 11:42:48 2021

@author: kariln
MATERIAL
"""
from functions import interpolate, column_check
from datetime import datetime

#DENSITY
def rho(data,density):
    now = datetime.now()
    print('Density: ' + str(now))
    data['density'] = density['rho'].iloc[0]
    return data

#SPECIFIC HEAT
def specific_heat(data,specificHeat):
    now = datetime.now()
    print('Specific heat: ' + str(now))
    column_check(data,['T_1'])
    data['cp'] = None
    for index,row in data.iterrows():
      prev_temp = row['T_1']
      for i,r in specificHeat.iterrows():
        if r['T'] > float(prev_temp) and i != 0:
          prev_r = specificHeat.loc[ i-1 , : ]
          if prev_r['cp'] == r['cp']:
            cp = r['cp']
          else:
            cp = interpolate(prev_r['cp'],r['cp'],prev_r['T'],r['T'],prev_temp)
          break
        elif float(prev_temp) < float(r['T']) and i == 0:
          cp = r['T']
          break
        elif i == specificHeat.index[-1]:
          cp= r['T']
          break
        else:
          continue
      data['cp'].iloc[index] = cp
    data.to_csv('disp_spec.csv', encoding='utf-8', index=False) 
    return data

#CONDUCTIVITY
def K(data,conductivity):
    now = datetime.now()
    print('Conductivity: ' + str(now))
    column_check(data,['T_1'])
    data['K'] = None
    for index,row in data.iterrows():
      prev_temp = row['T_1']
      for i,r in conductivity.iterrows():
        if r['T'] > float(prev_temp) and i != 0:
          prev_r = conductivity.loc[ i-1 , : ]
          if prev_r['K'] == r['K']:
            cond = r['K']
          else:
            cond = interpolate(prev_r['K'],r['K'],prev_r['T'],r['T'],prev_temp)
          break
        elif float(prev_temp) < float(r['T']) and i == 0:
          cond = r['T']
          break
        elif i == conductivity.index[-1]:
          cond = r['T']
          break
        else:
          continue
      data['K'].iloc[index] = cond
    data.to_csv('disp_cond.csv', encoding='utf-8', index=False) 
    return data

#THERMAL DIFFUSIVITY
def alpha(data):
    now = datetime.now()
    print('Diffusivity: ' + str(now))
    column_check(data,['K','cp','density'])
    data['diffusivity'] = None
    for index,row in data.iterrows():
      data['diffusivity'].iloc[index] = row['K']/(row['cp']*row['density'])
    data.to_csv('disp_diff.csv',encoding='utf-8',  index=False) 
    return data

def material(data,density,specificHeat,conductivity):
    now = datetime.now()
    print('Material: ' + str(now))
    data = rho(data,density)
    data = specific_heat(data,specificHeat)
    data = K(data,conductivity)
    data = alpha(data)
    return data
    