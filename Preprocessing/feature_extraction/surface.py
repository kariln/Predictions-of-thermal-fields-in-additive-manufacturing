# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:20:07 2021

@author: kariln
"""

from functions import column_check 
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.spatial import distance
import math

def on_surface(data, surf):
    now = datetime.now()
    print('Surface: ' + str(now))
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width']]
    i_unique = i_unique.drop_duplicates()
    on_surface = []
    for index,row in i_unique.iterrows():
        for i,r in surf.iterrows():
            if r['i'] == row['i']:
                on_surface.append(r['i'])
                break
    data['surface'] = 0
    for index,row in data.iterrows():
        if row['i'] in on_surface:
            data['surface'].iloc[index] = 1
    data.to_csv('disp_surface.csv',encoding='utf-8',  index=False) 
    return data

def surface_nodes(data, surf):
    now = datetime.now()
    print('Surface nodes: ' + str(now))
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width']]
    i_unique = i_unique.drop_duplicates()
    a = data['road_width'].iloc[0]
    lim = 3*a
    on_surface = pd.DataFrame(columns = ['i', 'surf_nr','surf_dst'])
    data['surf_nr'] = None
    data['surf_dist'] = None
    
    for index,row in i_unique.iterrows():
        print('Label: ' + str(row['i']))
        nr_nodes = 0
        dist = 0
        for i,r in surf.iterrows():
            if abs(r['x']-row['x'])<lim and abs(r['y']-row['y'])<lim and abs(r['z']-row['z'])<lim:
                nr_nodes += 1
                c = (r['x'], r['y'], r['z'])
                b = (row['x'], row['y'], row['z'])
                d = distance.euclidean(a, b)
                dist += abs(math.exp(-d**2).real)
        on_surface = on_surface.append({'i' : row['i'],'surf_nr' : nr_nodes,'surf_dst': dist} , ignore_index=True)
    for index,row in data.iterrows():
        print('index: ' + str(index))
        for i,r in on_surface.iterrows():
            if row['i'] == r['i']:
                data['surf_nr'].iloc[index] = r['surf_nr']
                data['surf_dist'].iloc[index] = r['surf_dst']
    data.to_csv('disp_surface_nr.csv',encoding='utf-8',  index=False) 
    return data

def SIZ_nodes(data):
    now = datetime.now()
    print('SIZ nodes: ' + str(now))
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width']]
    i_unique = i_unique.drop_duplicates()
    lim = 3*i_unique['road_width'].iloc[0]
    in_volume = pd.DataFrame(columns = ['i', 'vol_nr'])
    data['vol_nr'] = None
    for index,row in i_unique.iterrows():
        nr_nodes = 0
        for i,r in data.iterrows():
            if abs(r['x']-row['x'])<lim and abs(r['y']-row['y'])<lim and abs(r['z']-row['z'])<lim:
                nr_nodes += 1
        in_volume = in_volume.append({'i' : row['i'],'vol_nr' : nr_nodes} , ignore_index=True)
    for index,row in data.iterrows():
        for i,r in in_volume.iterrows():
            if row['i'] == r['i']:
                data['vol_nr'].iloc[index] = r['vol_nr']
    data.to_csv('disp_volume_nr.csv',encoding='utf-8',  index=False) 
    return data

#SURFACE INFLUENZE ZONE
def SIZ(data):
    now = datetime.now()
    print('SIZ: ' + str(now))
    column_check(data,['t','road_width','x','y','z','basedepth','globalseed','layer_thickness','vol_nr'])
    data['SIZ'] = None
    #time_steps = data['t'].unique()
    seed = data['globalseed'].iloc[0]
    layer_thickness = data['layer_thickness'].iloc[0]
    SIZ_V = 4/3*math.pi*(3*data['road_width'].iloc[0])**3
    SIZ_nodes_tot = SIZ_V*(seed**2*layer_thickness)
    base_height = data['basedepth'].iloc[0]
    
    for index,row in data.iterrows(): 
      n_nodes = row['vol_nr']
      if abs(row['z'] - base_height) < 3*row['road_width']: #checking if the substrate is within the SIZ
        h = 3*row['road_width'] - row['z'] + base_height # height of spherical cap
        r = 3*row['road_width']
        sub_V = math.pi*h**2/3*(3*r-h)
        sub_nodes = sub_V/(seed**2*layer_thickness)
        n_nodes += sub_nodes
      data['SIZ'].iloc[index] = n_nodes/SIZ_nodes_tot
      print('SIZ:'+ str(index))
    data.to_csv('disp_SIZ.csv',encoding='utf-8',  index=False) 
    return data


def SAV(data):
    now = datetime.now()
    print('SAV: ' + str(now))
    column_check(data,['vol_nr','surf_nr','layerNum','globalseed'])
    data['SAV'] = None
    exy = data['globalseed'].iloc[0]
    ez = data['layer_thickness'].iloc[0]
    approx_seed = (2*exy+ez)/3
    
    for index,row in data.iterrows():
        data['SAV'].iloc[index] = (row['surf_nr']/(approx_seed**2))/(row['vol_nr']/(exy**2*ez))
    data.to_csv('disp_SAV.csv',encoding='utf-8',  index=False) 
    return data

def surface(data,surf):
    data = on_surface(data,surf)
    data = surface_nodes(data, surf)
    data = SIZ_nodes(data)
    data = SIZ(data)
    data = SAV(data)
    return data

    