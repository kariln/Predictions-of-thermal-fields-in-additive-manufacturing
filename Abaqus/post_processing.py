# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:08:34 2020

@author: kariln
"""

from pathlib import Path
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

class Experiment:
    def __init__(self, exp_name, folder_name):
        self.exp_name = exp_name
        self.folder_name = folder_name

    def get_folder_name(self):
        return self.folder_name
    
    def get_exp_name(self):
        return self.exp_name
    
    def get_corner_file_path(self):
        exp_name = self.get_exp_name()
        foldername = self.get_folder_name()
        file_name = 'corner_node_'+exp_name + '.txt'
        file = os.path.join(os.path.dirname(os.path.abspath(__file__ )),"exp", foldername, file_name)
        return file
    
    def get_corner_node_data(self):
        file_path = self.get_corner_file_path()
        table = []
        with open(file_path, "r") as f: 
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table


    def get_property_table(self, material_property):
        file_path = self.get_property_file_path(material_property)
        table = []
        with open(file_path, "r") as f: 
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table
def main():
    zigzag = Experiment('zigzag','exp3')
    zigzag_corner = zigzag.get_corner_node_data()
    t_zigzag = [x[0] for x in zigzag_corner]
    temp_zigzag = [x[1] for x in zigzag_corner]
    raster = Experiment('raster','exp2')
    raster_corner = raster.get_corner_node_data()
    t_raster = [x[0] for x in raster_corner]
    temp_raster = [x[1] for x in raster_corner]
    
    degree_sign= u'\N{DEGREE SIGN}'
    mpl.style.use('seaborn-dark-palette')
    plt.plot(t_zigzag,temp_zigzag)
    plt.plot(t_raster,temp_raster)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C' + degree_sign + ']')
    plt.legend(['zigzag','raster'])
    axes = plt.gca()
    axes.set_xlim([100,200])
    axes.set_ylim([125,300])
    plt.savefig('cornernode_layer2')
    plt.show()
    
    
main()