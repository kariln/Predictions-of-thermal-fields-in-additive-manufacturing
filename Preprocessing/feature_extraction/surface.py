# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:20:07 2021

@author: kariln
"""

from functions import column_check 
from datetime import datetime
import pandas as pd
import numpy as np

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
    print(on_surface)
    data['surface'] = 0
    for index,row in data.iterrows():
        if row['i'] in on_surface:
            data['surface'].iloc[index] = 1
    data.to_csv('disp_surface.csv',encoding='utf-8',  index=False) 
    return data

def surface_nodes(data, surf):#må fikses
    now = datetime.now()
    print('Surface nodes: ' + str(now))
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width']]
    i_unique = i_unique.drop_duplicates()
    lim = 3*i_unique['road_width'].iloc[0]
    on_surface = pd.DataFrame(columns = ['i', 'surf_nr'])
    data['surf_nr'] = None
    for index,row in i_unique.iterrows():
        nr_nodes = 0
        for i,r in surf.iterrows():
            if abs(r['x']-row['x'])<lim and abs(r['y']-row['y'])<lim and abs(r['z']-row['z'])<lim:
                nr_nodes += 1
        on_surface = on_surface.append({'i' : row['i'],'surf_nr' : nr_nodes} , ignore_index=True)
    for index,row in data.iterrows():
        for i,r in on_surface.iterrows():
            if row['i'] == r['i']:
                data['surf_nr'].iloc[index] = r['surf_nr']
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


def SAV(data):
    now = datetime.now()
    print('SAV: ' + str(now))
    column_check(data,['vol_nr','surf_nr','layerNum','globalseed'])
    data['SAV'] = None
    approx_seed = (2*data['globalseed'].iloc[0]*data['layerNum'].iloc[0])
    for index,row in data.iterrows():
        data['SAV'].iloc[index] = row['surf_nr']/row['vol_nr']*approx_seed
    data.to_csv('disp_SAV.csv',encoding='utf-8',  index=False) 
    return data

    