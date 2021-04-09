# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:04:09 2021

@author: kariln
PREPROCESSING
"""

from deposition_properties import deposition_properties
from spatial import spatial
from functions import dataframe_creation
from thermal import thermal
from material import material
from heat import heat
from improve_data import improve

from datetime import datetime

def preprocessing(filename: str, v: float, road_width: float, nr_layers: int, layer_thickness: float, base_height: float, seed: float):
    now = datetime.now()
    print('Start: ' + str(now))
    data, dp, dm, conductivity, density, specificHeat = dataframe_creation(filename) #creating the necessary dataframes
    data = deposition_properties(data,dp,dm,v, road_width)
    data = spatial(data, nr_layers, layer_thickness, base_height)
    data = thermal(data)
    data = material(data,density,specificHeat,conductivity)
    data = heat(data,seed, base_height)
    data = improve(data)
    data.to_csv('preprocessed.csv',encoding='utf-8',  index=False) 
    return data
def main():
    data = preprocessing('disp.txt', 0.015, 0.01, 4, 0.0023, 0.02,0.0023)
    print(data.head())

main()
    

