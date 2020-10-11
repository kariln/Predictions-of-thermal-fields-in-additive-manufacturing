# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 13:17:26 2020

@author: Kari Ness
"""
import os 

class Material:
    def __init__(self,material_properties, material_name):
        #The material_properties should be a list of strings containing material property types
        self.material_properties = material_properties
        
        #The material should be a string
        self.material_name = material_name
        
    def get_material_name(self):
        return self.material_name
        
    def get_property_file(self, material_property):
        file_name = self.get_material_name() + '_' + material_property + '.txt'
        #file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), file_name)
        file = os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), file_name)
        return file
    
    def get_property_table(self, material_property):
        file = self.get_property_file(material_property)
        table = []
        with open(file,"r") as f:
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table