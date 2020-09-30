# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:39:34 2020

@author: Kari Ness
"""

import pattern
import copy

#Raster deposition pattern
class Raster(pattern.Pattern):
    
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P)
          
    def pass_time(self):
      return self.get_length()[self.get_deposition_dir()]/self.get_velocity()
  
    def nr_passes(self):
        return self.get_transverse_dir()/self.get_road_width()
        
    def get_print_coord(self):
        #coord = [x,y,z_heat,z_material]
        coord = [self.get_corner_coord()[0],self.get_corner_coord()[1],self.get_corner_coord()[2],self.get_corner_coord()[2]]
        coord[self.get_deposition_dir()] += self.get_road_width()/2
        coord[self.get_stack_dir()] += self.get_thickness()
        coord[self.get_stack_dir()] += self.get_thickness()/2
        return coord

    def generate_heat_path(self):
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      pass_time = self.pass_time()
      reverse_time = pass_time/10
      P = self.get_power()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord()
      
      start = copy.deepcopy(coord)
      
      #creating text files for heat and material path
      heat_path = open("heat_path.txt","w+")
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              heat_path.write(self.coord_string(time,coord[0],coord[1], coord[2], P))
              coord[0] += self.get_x_length()
              time += pass_time
              heat_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
              coord[0] -= self.get_x_length()
              coord[1] += self.get_road_width()
              time += reverse_time
          coord[1] = start[1]
          coord[0] = start[0]
          coord[2] += self.get_thickness()
          
    def generate_material_path(self):
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      pass_time = self.pass_time()
      reverse_time = pass_time/10
      A = self.get_area()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord()
      
      start = copy.deepcopy(coord)
      
      #creating text files for heat and material path
      material_path = open("heat_path.txt","w+")
      
      material_path = open("material_path.txt","w+")
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              material_path.write(self.coord_string(time,coord[0],coord[1], coord[3], A))
              coord[0] += self.get_x_length()
              time += pass_time
              material_path.write(self.coord_string(time,coord[0],coord[1],coord[3],0))
              coord[0] -= self.get_x_length()
              coord[1] += self.get_road_width()
              time += reverse_time
          coord[1] = start[1]
          coord[0] = start[0]
          coord[3] += self.get_thickness()

                
def main():        
    raster = Raster(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,5000)
    raster.generate_heat_path()
    raster.generate_material_path()
main()