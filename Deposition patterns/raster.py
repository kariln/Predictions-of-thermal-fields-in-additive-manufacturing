# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:39:34 2020

@author: Kari Ness
"""

import pattern
class Raster(pattern.Pattern):
    
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P)
    
    def nr_passes(self):
        if self.get_stack_dir == 1:
            if self.get_start_dir ==2:
                return self.get_z_length/self.get_road_width
            else:
                return self.get_y_length/self.get_road_width
            
        if self.get_stack_dir == 2:
            if self.get_start_dir ==1:
                return self.get_z_length/self.get_road_width
            else:
                return self.get_x_length/self.get_road_width
            
        if self.get_stack_dir == 3:
            if self.get_start_dir ==2:
                return self.get_x_length/self.get_road_width
            else:
                return self.get_y_length/self.get_road_width
            
    def get_print_start(self):
        if self.get_start_dir == 1 and self.get_stack_dir == 3:
            x = self.get_start_coord[0] 
            y = self.get_start_coord[1] + self.get_road_width/2
            z_heat = self.get_start_coord[2] + self.get_thickness
            z_material = self.get_start_coord[2] + self.get_thickness/2
            
        if self.get_start_dir == 2 and self.get_stack_dir == 3:
            x = self.get_start_coord[0] + self.get_road_width/2
            y = self.get_start_coord[1] 
            z_heat = self.get_start_coord[2] + self.get_thickness
            z_material = self.get_start_coord[2] + self.get_thickness/2
        
    
    def generate_path(self):
        #creating text files for heat and material path
        create_files()
        
        layers = self.get_layer_nr
        passes = self.nr_passes
        time = 0
        
        #setting the start coordinate of the raster
        if self.get_start_dir == 1 and self.get_stack_dir == 3:
            x = self.get_start_coord[0] 
            y = self.get_start_coord[1] + self.get_road_width/2
            z_heat = self.get_start_coord[2] + self.get_thickness
            z_material = self.get_start_coord[2] + self.get_thickness/2
        
        for i in range(0,layers):
            for j in range(0,passes):
                print("hei")
                
def main():        
    raster = Raster(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,500)
    print(raster.get_z_length())
main()