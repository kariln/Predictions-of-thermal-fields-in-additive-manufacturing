# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:39:34 2020

@author: Kari Ness
"""

import zigzag

class Raster(zigzag.Zigzag):
    
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P)
        
    
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
              path.append([time,coord[0],coord[1],coord[2],0])
              coord[self.get_transverse_dir()] += self.get_road_width()
              coord[self.get_deposition_dir] -= self.get_length()[self.get_deposition_dir()]
              time += up_time
          coord[self.get_deposition_dir()] = start[self.get_deposition_dir()]
          coord[self.get_transverse_dir()] = start[self.get_transverse_dir()]
          coord[self.get_stack_dir()] += self.get_thickness()
        return path


    def generate_heat_path(self):
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      pass_time = self.pass_time()
      reverse_time = pass_time/10
      P = self.get_power()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord(0)
      
      start = self.get_print_coord(0)
      
      #creating text files for heat and material path
      heat_path = open("heat_path.txt","w+")
      heat_path.truncate(0)  
         
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
=======
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
        passes = self.nr_passes()
        pass_time = self.pass_time()
        up_time = self.up_time()

    def generate_heat_path(self):
>>>>>>> parent of 450d73d... .
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      pass_time = self.pass_time()
      reverse_time = pass_time/10
<<<<<<< HEAD
      A = self.get_area()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord(1)
      
      start = self.get_print_coord(1)
      
      #creating text files for heat and material path
      material_path = open("heat_path.txt","w+")
      material_path.truncate(0)  
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              material_path.write(self.coord_string(time,coord[0],coord[1], coord[2], A))
              coord[0] += self.get_x_length()
              time += pass_time
<<<<<<< HEAD
              material_path.write(self.coord_string(time,coord[0],coord[1],coord[3],0))
=======
      P = self.get_power()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord(0)
      
      start = self.get_print_coord(0)
      
      #creating text files for heat and material path
      heat_path = open("heat_path.txt","w+")
      heat_path.truncate(0)  
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              heat_path.write(self.coord_string(time,coord[0],coord[1], coord[2], P))
              coord[0] += self.get_x_length()
              time += pass_time
              heat_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
>>>>>>> parent of 450d73d... .
=======
              material_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
>>>>>>> parent of 8552fb5... .
              coord[0] -= self.get_x_length()
              coord[1] += self.get_road_width()
              time += reverse_time
          coord[1] = start[1]
          coord[0] = start[0]
<<<<<<< HEAD
<<<<<<< HEAD
          coord[3] += self.get_thickness()
=======
          coord[2] += self.get_thickness()
          
    def generate_material_path(self):
      layers = self.get_layer_nr()
      passes = self.nr_passes()
      time = 0
      pass_time = self.pass_time()
      reverse_time = pass_time/10
      A = self.get_area()
        
      #setting the start coordinate of the raster
      coord = self.get_print_coord(1)
      
      start = self.get_print_coord(1)
      
      #creating text files for heat and material path
      material_path = open("heat_path.txt","w+")
      material_path.truncate(0)  
         
      for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              material_path.write(self.coord_string(time,coord[0],coord[1], coord[2], A))
              coord[0] += self.get_x_length()
              time += pass_time
              material_path.write(self.coord_string(time,coord[0],coord[1],coord[2],0))
              coord[0] -= self.get_x_length()
              coord[1] += self.get_road_width()
              time += reverse_time
          coord[1] = start[1]
          coord[0] = start[0]
          coord[2] += self.get_thickness()
>>>>>>> parent of 450d73d... .
=======
          coord[2] += self.get_thickness()
>>>>>>> parent of 8552fb5... .

                
def main():        
    raster = Raster(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,5000)
    raster.generate_heat_path()
    raster.generate_material_path()
main()