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
            
        elif self.get_stack_dir == 2:
            if self.get_start_dir ==1:
                return self.get_z_length/self.get_road_width
            else:
                return self.get_x_length/self.get_road_width
            
        else:
            if self.get_start_dir ==2:
                return self.get_x_length/self.get_road_width
            else:
                return self.get_y_length()/self.get_road_width()
            
    def get_print_coord(self):
        #default start direction and stack direction
        if self.get_start_dir() == 1 and self.get_stack_dir() == 3:
            x = self.get_corner_coord()[0] 
            y = self.get_corner_coord()[1] + self.get_road_width()/2
            z_heat = self.get_corner_coord()[2] + self.get_thickness()
            z_material = self.get_corner_coord()[2] + self.get_thickness()/2
            return x,y,z_heat,z_material
            
        elif self.get_start_dir == 2 and self.get_stack_dir == 3:
            x = self.get_corner_coord[0] + self.get_road_width/2
            y = self.get_corner_coord[1] 
            z_heat = self.get_corner_coord[2] + self.get_thickness
            z_material = self.get_corner_coord[2] + self.get_thickness/2
            return [x,y,z_heat,z_material]
            
        else:
            raise ValueError("The combination of start direction and stack direction is not implemented.")
        
    def coord_string(self,t,x,y,z,p):
      temp= "{},{},{},{},{}"
      return temp.format(t,x,y,z,p)
  
    def generate_path(self):
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      A = self.get_area()
      P = self.get_power()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord()
      
      #creating text files for heat and material path
      print("hei")
      heat_path = open("heat_path.txt","w+")
      heat_path.write(self.coord_string(time,coord[0],coord[1], coord[2], P))
      material_path = open("heat_path.txt","w+")
      material_path.write(self.coord_string(time,coord[0],coord[1],coord[3], A))
         
#      for i in range(0,layers):
#          for j in range(0,passes):
#              print("hei")
                
def main():        
    raster = Raster(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,500)
    print(raster.get_stack_dir())
    print(raster.get_start_dir())
    print(raster.get_print_coord())
    sting = raster.coord_string(1,2,3,4,5)
    print(sting)
    print(raster.generate_path())
main()