# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:42:38 2021

@author: kariln
"""
from functions import frame_creation
import pandas as pd
filename = 's-heat.txt'
heat1 = pd.read_csv(filename, header = None, names= ['t','x','y','z','Q'])
filename = 's-material.txt'
material1=pd.read_csv(filename, header = None, names = ['t','x','y','z','A'])
heat_tmp = pd.read_csv('heat3.txt', header = None, names = ['t','x','y','z','A'])
heat2 = pd.DataFrame(columns=['t','x','y','z','Q'])
material2 = pd.DataFrame(columns=['t','x','y','z','A'])

time = heat1['t'].iloc[-1] + 10

for index,row in heat1.iterrows(): 
    heat2 = heat2.append({'t' : row['t'] + time*3,'x' : row['x'],'y' : row['y'],'z' : row['z']*4,'Q' : row['Q']}, ignore_index = True)
    material2 = material2.append({'t' : row['t'] + time*3,'x' : row['x'],'y' : row['y'],'z' : row['z']*4,'A' : material1['A'].iloc[index]}, ignore_index = True)

heat2.to_csv('heat4.txt', header=None, index=None, sep=',', mode='a')
material2.to_csv('material4.txt', header=None, index=None, sep=',', mode='a')