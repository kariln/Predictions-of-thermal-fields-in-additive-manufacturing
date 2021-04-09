# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:01:22 2021

@author: kariln
"""
import pandas as pd
import numpy as np
from datetime import datetime

def interpolate(x1: float, x2: float, y1: float, y2: float, x: float):
    """Perform linear interpolation for x between (x1,y1) and (x2,y2) """
    return ((y2 - y1) * x + x2 * y1 - x1 * y2) / (x2 - x1)

def dataframe_creation(filename:str):
    now = datetime.now()
    print('Dataframe creation: ' + str(now))
    data = pd.read_csv(filename, header = 0, sep=',', index_col=False) #dataset
    dp = pd.read_csv('heat_path.txt', sep=",", header=None, names=["t","x","y","z","Q"]) #heat path 
    dm = pd.read_csv('material_path.txt', sep=",", header=None, names=["t","x","y","z","A"]) #material path
    conductivity = pd.read_csv('AA2319_Conductivity.txt', names=["T","cond"])
    density = pd.read_csv('AA2319_Density.txt', names=["rho"])
    specificHeat = pd.read_csv('AA2319_SpecificHeat.txt', names=["T","cp"])
    return data, dp, dm, conductivity, density, specificHeat

def column_check(data, column_names):
    #checking it the necessary columns exists
    for name in column_names:    
        if name not in data.columns:
            diff = np.setdiff1d(column_names,data.columns) # finds the columns that are not present in dataframe
            raise ValueError('The dataframe does not contain the necessary columns. Add: ' + str(diff))

def frame_creation( filename:str):
    now = datetime.now()
    print('Dataframe creation: ' + str(now))
    data = pd.read_csv(filename, header = 0, sep=',', index_col=False) #dataset
    return data
