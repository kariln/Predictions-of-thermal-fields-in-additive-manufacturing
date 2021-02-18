# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:49:06 2021

@author: Kari Ness
"""

import pattern

#In-Out deposition pattern
class In_Out(pattern.Pattern):
    def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break):
        super().__init__(z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P, layer_break)

    def pass_time(self):
        return self.get_length()[self.get_deposition_dir()]/self.get_velocity()

    def get_rounds(self):
        lengths = self.get_length()
        length_x = lengths[0]
        length_y = lengths[1]
        return (length_x+length_y)/self.get_road_width()
    
    def get_print_coord(self):#input 0 for heat, 1 for material
        #coord = [x,y,z]
        coord = [self.get_corner_coord()[0],self.get_corner_coord()[1],self.get_corner_coord()[2]]
        coord[self.get_transverse_dir()] += self.get_road_width()/2
        coord[self.get_stack_dir()] += self.get_thickness()
        return coord
    
    def get_coord(self):
        coord = [self.get_corner_coord()[0],self.get_corner_coord()[1],self.get_corner_coord()[2]]
        return coord

    def get_path(self):
        #setting the start coordinate of the inout
        coord = self.get_print_coord()
        
        #initial conditions:
        start = self.get_print_coord()
        P = self.get_power()
        A = self.get_area()
        time = 0
        direction = 1 #defines if the deposition moves forward or backwards
        path = []
        
        layers = self.get_layer_nr()
        road_width = self.get_road_width()
        rounds = self.get_rounds()
        
        length = self.get_length()
        
        for i in range(0,int(layers)):
            for j in range(0,int(rounds)):
                path.append([time,coord[0],coord[1], coord[2], P,A])
                if j == 0:
                    length[self.get_deposition_dir()] -=road_width/2
                else:
                    length[self.get_deposition_dir()] -=road_width
                coord[self.get_deposition_dir()] += direction*(self.get_length()[self.get_deposition_dir()])
                self.set_axis(self.get_transverse_dir(),self.get_deposition_dir(),self.get_stack_dir())
                pass_time = self.pass_time()
                time += pass_time
                if j != 0 and j%2 != 0:
                    direction = direction*(-1)
            P = P*0.995
            coord[self.get_deposition_dir()] = start[self.get_deposition_dir()]
            coord[self.get_transverse_dir()] = start[self.get_transverse_dir()]
            coord[self.get_stack_dir()] = self.get_thickness() + coord[self.get_stack_dir()]
            time += self.get_layer_break()

        return path


    
    def set_length(self,x_length,y_length):
        self.length = [x_length,y_length, self.get_length()[2]]

def main():        
    inout = In_Out(0.06, 0.01, 0.06, 0.06, -0.03, -0.03, 0.02, 0.01,5000,10)
    path_list = inout.get_path()
    print(path_list)
    #print(path_list)
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
    print(x)
    print(y)
    inout.generate_heat_path()
    inout.generate_material_path()
main()
    