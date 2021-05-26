# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:06:34 2021

@author: kariln
"""
import math
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from functions import column_check 
from datetime import datetime
import pandas as pd

def tetrahedron_volume(a, b, c, d):
    return np.abs(np.einsum('ij,ij->i', a-d, np.cross(b-d, c-d))) / 6

def convex_hull_volume(pts):
    ch = ConvexHull(pts)
    dt = Delaunay(pts[ch.vertices])
    tets = dt.points[dt.simplices]
    return np.sum(tetrahedron_volume(tets[:, 0], tets[:, 1],
                                     tets[:, 2], tets[:, 3]))

def convex_hull_volume_bis(pts):
    ch = ConvexHull(pts)

    simplices = np.column_stack((np.repeat(ch.vertices[0], ch.nsimplex),
                                 ch.simplices))
    tets = ch.points[simplices]
    return np.sum(tetrahedron_volume(tets[:, 0], tets[:, 1],
                                     tets[:, 2], tets[:, 3]))


def SIZ_volume(data):
    now = datetime.now()
    print('Surface nodes: ' + str(now))
    data['VR'] = None
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width','VR']]
    i_unique = i_unique.drop_duplicates()
    i_unique = i_unique.reset_index()
    a = data['road_width'].iloc[0]
    lim = 3*a
    SIZ_V = 4/3*math.pi*(3*data['road_width'].iloc[0])**3
    base_height = data['basedepth'].iloc[0]
    label_nr = i_unique.shape[0]
    for index,row in i_unique.iterrows():
        print('label: ' + str(index) + ' of ' + str(label_nr))
        sub_V = 0
        SIZ_nodes = []
        for i,r in i_unique.iterrows():
            if abs(r['x']-row['x'])<lim and abs(r['y']-row['y'])<lim and abs(r['z']-row['z'])<lim:
                SIZ_nodes.append([r['x'],r['y'],r['z']])
        volume = convex_hull_volume_bis(SIZ_nodes)
        if abs(row['z'] - base_height) < lim: #checking if the substrate is within the SIZ
            h = 3*row['road_width'] - row['z'] + base_height # height of spherical cap
            sub_V = math.pi*h**2/3*(3*lim-h)
        i_unique['VR'].iloc[index] = (volume+sub_V)/SIZ_V
    index = 0
    for j,row in data.iterrows():
        print('index: ' + str(index))
        for i,r in i_unique.iterrows():
            if row['i'] == r['i']:
                data['VR'].iloc[index] = r['VR']
        index += 1
    data.to_csv('disp_SIZ_V.csv',encoding='utf-8',  index=False) 
    return data

def SIZ_volume2(data):
    now = datetime.now()
    print('Surface nodes: ' + str(now))
    data['VR'] = None
    column_check(data,['t','x','y','z','road_width'])
    i_unique = data[['i', 'x','y','z','road_width','VR']]
    i_unique = i_unique.drop_duplicates()
    i_unique = i_unique.reset_index()
    a = data['road_width'].iloc[0]
    lim = 3*a
    SIZ_V = 4/3*math.pi*(3*data['road_width'].iloc[0])**3
    base_height = data['basedepth'].iloc[0]
    label_nr = i_unique.shape[0]
    for index,row in i_unique.iterrows():
        print('label: ' + str(index) + ' of ' + str(label_nr))
        sub_V = 0
        SIZ_nodes = []
        for i,r in i_unique.iterrows():
            if abs(r['x']-row['x'])<lim and abs(r['y']-row['y'])<lim and abs(r['z']-row['z'])<lim:
                SIZ_nodes.append([r['x'],r['y'],r['z']])
        volume = convex_hull_volume_bis(SIZ_nodes)
        if abs(row['z'] - base_height) < lim: #checking if the substrate is within the SIZ
            h = 3*row['road_width'] - row['z'] + base_height # height of spherical cap
            sub_V = math.pi*h**2/3*(3*lim-h)
        i_unique['VR'].iloc[index] = (volume+sub_V)/SIZ_V
        data.loc[data['i'] == row['i'], 'VR'] = (volume+sub_V)/SIZ_V
        print(data['VR'].isnull().sum())
    data.to_csv('disp_SIZ_V2.csv',encoding='utf-8',  index=False) 
    return data



# def SIZ_volume(data):
#     now = datetime.now()
#     print('SIZ_volume: ' + str(now))
#     column_check(data,['t','road_width','x','y','z','basedepth','globalseed','layer_thickness','vol_nr'])
#     data['SIZ'] = None
#     layer_thickness = data['layer_thickness'].iloc[0]
#     SIZ_V = 4/3*math.pi*(3*data['road_width'].iloc[0])**3
#     base_height = data['basedepth'].iloc[0]
    
#     for index,row in data.iterrows(): 
#       n_nodes = row['vol_nr']
#       if abs(row['z'] - base_height) < 3*row['road_width']: #checking if the substrate is within the SIZ
#         h = 3*row['road_width'] - row['z'] + base_height # height of spherical cap
#         r = 3*row['road_width']
#         sub_V = math.pi*h**2/3*(3*r-h)
#         sub_nodes = sub_V/(seed**2*layer_thickness)
#         n_nodes += sub_nodes
#       data['SIZ'].iloc[index] = n_nodes/SIZ_nodes_tot
#       print('SIZ:'+ str(index))
#     data.to_csv('disp_SIZ.csv',encoding='utf-8',  index=False) 
#     return data
