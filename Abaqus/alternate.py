# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:57:46 2021

@author: kariln
"""

import zigzag

class Raster(zigzag.Zigzag):
    
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P,layer_break,velocity):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P,layer_break,velocity)
        
    
    def get_path(self):
        #setting the start coordinate of the raster
        coord = self.get_print_coord()
      
        #initial conditions:
        start = self.get_print_coord()
        
        P = self.get_power()
        A = self.get_area()
        time = 0
        path = []
        
        layers = self.get_layer_nr()
        passes = self.nr_passes()
        pass_time = self.pass_time()
        up_time = self.up_time()
        
        for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              path.append([time,coord[0],coord[1], coord[2], P,A])
              coord[self.get_deposition_dir()] += self.get_length()[self.get_deposition_dir()]
              time += pass_time
              path.append([time,coord[0],coord[1],coord[2],0,0])
              coord[self.get_transverse_dir()] += self.get_road_width()
              coord[self.get_deposition_dir()] -= self.get_length()[self.get_deposition_dir()]
              time += up_time
              #P = P*0.995
          coord[self.get_deposition_dir()] = start[self.get_deposition_dir()]
          coord[self.get_transverse_dir()] = start[self.get_transverse_dir()]
          coord[self.get_stack_dir()] += self.get_thickness()
        return path
                
#def main():        
#    raster = Raster(0.012, 0.002, 0.06, 0.06, -0.03, -0.03, 0.02, 0.002,500)
#    raster.generate_heat_path()
#    raster.generate_material_path()
#main()