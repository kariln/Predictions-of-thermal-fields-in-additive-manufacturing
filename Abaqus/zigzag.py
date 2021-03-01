# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:30:43 2021

@author: kariln
"""

import pattern

#Zig-Zag deposition pattern
class Zigzag(pattern.Pattern):
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break)

    def pass_time(self):
        return self.get_length()[self.get_deposition_dir()]/self.get_velocity()
    
    def up_time(self):
        return (self.get_road_width()/(self.get_velocity()))/10
  
    def nr_passes(self):
        return int(self.get_length()[self.get_transverse_dir()]/self.get_road_width())
        
    def get_print_coord(self):#input 0 for heat, 1 for material
        #coord = [x,y,z]
        coord = [self.get_corner_coord()[0],self.get_corner_coord()[1],self.get_corner_coord()[2],self.get_corner_coord()[2]]
        coord[self.get_transverse_dir()] += self.get_road_width()/2
        coord[self.get_stack_dir()] += self.get_thickness()
        return coord
    
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
        
        for i in range(0,int(layers)):
          for j in range(0,int(passes)):
              path.append([time,coord[0],coord[1], coord[2], P,A])
              coord[self.get_deposition_dir()] += direction*self.get_length()[self.get_deposition_dir()]
              direction = direction*(-1)
              time += pass_time
              path.append([time,coord[0],coord[1],coord[2],0,0])
              coord[self.get_transverse_dir()] += self.get_road_width()
              time += up_time
              
          coord[self.get_deposition_dir()] = start[self.get_deposition_dir()]
          coord[self.get_transverse_dir()] = start[self.get_transverse_dir()]
          coord[self.get_stack_dir()] = self.get_thickness() + coord[self.get_stack_dir()]
          time += self.get_layer_break()
          P = 0.9*P
        return path


def main():        
    zigzag = Zigzag(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,5000,10)
    zigzag.generate_heat_path()
    zigzag.generate_material_path()
    path_list = zigzag.get_path()
    import matplotlib.pyplot as plt
    x = []
    y = []
    z = 0.03
    for elem in path_list:
        if z != elem[3]:
            break
        x.append(elem[1])
        y.append(elem[2])
        
    plt.plot(x,y)
    plt.xlim(-0.03,0.03)
    plt.ylim(-0.03,0.03)
main()