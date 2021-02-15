# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:49:06 2021

@author: Kari Ness
"""

import pattern

#Zig-Zag deposition pattern
class In_Out(pattern.Pattern):
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break)

    def get_path(self):
        #setting the start coordinate of the raster
        coord = self.get_print_coord()
        
        #initial conditions:
        start = self.get_print_coord()
        P = self.get_power()
        A = self.get_area()
        time = 0
        direction = 1 #defines if the deposition moves forward or backwards
        path = []
        
        layers = self.get_layer_nr()
        pass_time = self.pass_time()
        up_time = self.up_time()
        #JOBB VIDERE
        return path
    
    def up_time(self):
        return (self.get_road_width()/(self.get_velocity()))/10
    
    def pass_time(self):
        return self.get_length()[self.get_deposition_dir()]/self.get_velocity()
    
    def set_length(self,x_length,y_length):
        self.length = [x_length,y_length, self.get_length()[2]]
        
    