# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 20:50:49 2020

@author: Kari Ness
"""
import pattern
import copy

#Zig-Zag deposition pattern
class Zigzag(pattern.Pattern):
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P)

    def pass_time(self):
        return self.get_length()[self.get_deposition_dir()]/self.get_velocity()
    
    def up_time(self):
        return (self.get_road_width()/(self.get_velocity()))/10
  
    def nr_passes(self):
        return self.get_transverse_dir()/self.get_road_width()
        
    def get_print_coord(self, inp):#input 0 for heat, 1 for material
        #coord = [x,y,z]
        coord = [self.get_corner_coord()[0],self.get_corner_coord()[1],self.get_corner_coord()[2],self.get_corner_coord()[2]]
        coord[self.get_transverse_dir()] += self.get_road_width()/2
        if inp == 0:
            coord[self.get_stack_dir()] += self.get_thickness()
        else:
            coord[self.get_stack_dir()] += self.get_thickness()/2
        return coord

    def generate_heat_path(self):
      #setting the start coordinate of the raster
      coord = self.get_print_coord(0)
      
      #initial conditions:
      start = copy.deepcopy(coord)
      time = 0
      direction = 1 #defines if the deposition moves forward or backwards
      
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      pass_time = self.pass_time()
      up_time = self.up_time()
      P = self.get_power()
      
      #creating text files for heat and material path
      heat_path = open("heat_path.txt","w+")
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              heat_path.write(self.coord_string(time,coord[0],coord[1], coord[2], P))
              coord[self.get_deposition_dir()] += direction*self.get_length()[self.get_deposition_dir()]
              direction = direction*(-1)
              time += pass_time
              heat_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
              coord[self.get_transverse_dir()] += self.get_road_width()
              time += up_time
          coord[self.get_deposition_dir()] = start[self.get_deposition_dir()]
          coord[self.get_transverse_dir()] = start[self.get_transverse_dir()]
          coord[self.get_stack_dir()] += self.get_thickness()
          
    def generate_material_path(self):
      #setting the start coordinate of the raster
      coord = self.get_print_coord(1)
      
      #initial conditions:
      start = copy.deepcopy(coord)
      time = 0
      direction = 1 #defines if the deposition moves forward or backwards
      
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      pass_time = self.pass_time()
      up_time = self.up_time()
      A = self.get_area()

      material_path = open("material_path.txt","w+")
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              material_path.write(self.coord_string(time,coord[0],coord[1], coord[2], A))
              coord[0] += direction*self.get_x_length()
              direction = direction*(-1)
              time += pass_time
              material_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
              coord[1] += self.get_road_width()
              time += up_time
          coord[1] = start[1]
          coord[0] = start[0]
          coord[2] += self.get_thickness()

                
def main():        
    zigzag = Zigzag(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,5000)
    zigzag.generate_heat_path()
    zigzag.generate_material_path()
main()