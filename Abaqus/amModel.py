# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:17:14 2020

@author: Kari Ness
"""

class AM:
    def __init__(self,part, amModel_name):
        self.part = part
        self.amModel_name = amModel_name 
        self.road_width = None
        self.activation_offset = None
        self.absorption_coefficient = None

    def get_part(self):
        return self.part
    
    def get_part_name(self):
        return self.get_part().get_part_name()
    
    def get_amModel_name(self):
        return self.amModel_name
    
    def set_road_width(self,road_width):
        self.road_width = road_width
        
    def get_road_width(self):
        return self.road_width
        
    def set_activation_offset(self, activation_offset):
        self.activation_offset = activation_offset
        
    def set_absorption_coefficient(self,absorption_coefficient):
        self.absorption_coefficient = absorption_coefficient