# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 16:47:02 2021

@author: kariln
"""
import sys
sys.path.append(r'C:\Users\kariln\Documents\GitHub\Master\Preprocessing')
from feature_extraction import *
from functions import dataframe_creation

# from deposition_properties import deposition_properties
# from spatial import euclid_grad,laser_dir
# from functions import dataframe_creation
# from thermal import temp_stat
# from material import material
# from heat import SIZ
# from improve_data import improve

from datetime import datetime

def prep(filename: str, v: float, road_width: float, nr_layers: int, layer_thickness: float, base_height: float, seed: float):
    now = datetime.now()
    print('Start: ' + str(now))
    data, dp, dm, conductivity, density, specificHeat = dataframe_creation(filename) 
    data = euclid_grad(data)
    data = laser_dir(data)
    data = temp_stat(data)
    data = SIZ(data,seed, base_height)
    data.to_csv('preprocessed.csv',encoding='utf-8',  index=False) 
    return data
def main():
    data = prep('disp_euclid (5).csv', 0.015, 0.002, 1, 0.0023, 0.005,0.00023)
    print(data.head())

main()