# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:19:37 2021

@author: kariln
"""

#Creating circular printing pattern
import numpy as np
import matplotlib.pyplot as plt

def circle_path(radius, seeds, area,power):
    path_X = []
    path_Y = []
    path_A = []
    path_Q = []
    x = radius #starting point, X
    y = 0 #starting point, Y
    for i in range(1,seeds+1):
        path_X.append(x)
        path_Y.append(y)
        path_A.append(area)
        path_Q.append(power)
        x = np.cos(2*np.pi/seeds*i)*radius
        y = np.sin(2*np.pi/seeds*i)*radius
    path_X.append(radius)
    path_Y.append(0)
    path_A.append(0)
    path_Q.append(0)
    return path_X,path_Y,path_A,path_Q

def circle_time(path_X,path_Y,velocity, t_start):
    t = t_start
    path_t = []
    path_t.append(t)
    for i in range(0,len(path_X)-1):
        a = path_X[i+1]-path_X[i]
        b = path_Y[i+1]-path_Y[i]
        c = np.sqrt(a**2+b**2)
        t += c/velocity
        path_t.append(t)
    return path_t

def generate_heat_path(power, path_X,path_Y,path_t, path_Q,z):
    heat_path = open("heat_path.txt","a")
    for i in range(0,len(path_X)):
        heat_path.write(coord_string(path_t[i], path_X[i], path_Y[i], z, path_Q[i]))
        
def generate_material_path(area, path_X,path_Y,path_t, path_A,z):
    material_path = open("material_path.txt","a")
    for i in range(0,len(path_X)):
        material_path.write(coord_string(path_t[i], path_X[i], path_Y[i], z, path_A[i]))

def coord_string(t,x,y,z,p):
    temp= "{},{},{},{},{}\n"
    return temp.format(t,x,y,z,p)
  
def main():
    layer_thickness = 0.0023
    base_height = 0.02
    road_width = 0.01
    power = 4500
    area = road_width*layer_thickness
    radius = 0.015
    t_start = 0
    heat_path = open("heat_path.txt","a")
    heat_path.truncate(0) 
    material_path = open("material_path.txt","a")
    material_path.truncate(0)
    nr_layers = 4
    height = layer_thickness + base_height
    for j in range(nr_layers):
        for i in range(0,5):
            #CIRCLE
            path_X,path_Y,path_A,path_Q = circle_path(radius,100,area,power)
            path_t = circle_time(path_X,path_Y,0.015,t_start)
            heat_path = open("heat_path.txt","a")
            generate_heat_path(power, path_X, path_Y, path_t, path_Q,height)
            material_path = open("material_path.txt","a")
            generate_material_path(area, path_X, path_Y, path_t, path_A,height)
            
            #BREAK
            radius += 0.01
            t_start = path_t[-1] + 2
            #heat_path.write(coord_string(t_start,radius,0,height,0))
            #material_path.write(coord_string(t_start,radius,0,height,0))
            
        
        height += layer_thickness
        #BREAK
        t_start = path_t[-1] + 10
        heat_path.write(coord_string(t_start,radius,0,height,0))
        material_path.write(coord_string(t_start,radius,0,height,0))
        radius = 0.015
        t_start = t_start +10
    

    # for i in range(0,6):
    #     #CIRCLE
    #     path_X,path_Y,path_A,path_Q = circle_path(radius,100,area,power)
    #     path_t = circle_time(path_X,path_Y,0.015,t_start)
    #     heat_path = open("heat_path.txt","a")
    #     generate_heat_path(power, path_X, path_Y, path_t, path_Q,height)
    #     material_path = open("material_path.txt","a")
    #     generate_material_path(area, path_X, path_Y, path_t, path_A,height)
        
    #     #BREAK
    #     radius += 0.01
    #     t_start = path_t[-1] + 1
    #     heat_path.write(coord_string(t_start,radius,0,height,power))
    #     material_path.write(coord_string(t_start,radius,0,height,area))
            
    # #FIRST CIRCLE
    # path_X,path_Y,path_A,path_Q = circle_path(0.003,30,area,power)
    # path_t = circle_time(path_X,path_Y,0.015,0)
    
    # heat_path = open("heat_path.txt","a")
    # heat_path.truncate(0)  
    # generate_heat_path(power, path_X, path_Y, path_t, path_Q)
    
    # material_path = open("material_path.txt","a")
    # material_path.truncate(0)  
    # generate_material_path(area, path_X, path_Y, path_t, path_A)
    
    # # #BREAK
    # t_start = path_t[-1] + 1
    # heat_path.write(coord_string(t_start,0.005,0,7.3*10**(-3),power))
    # material_path.write(coord_string(t_start,0.005,0,7.3*10**(-3),area))
    
    # #SECOND CIRCLE
    # path_X,path_Y,path_A,path_Q = circle_path(0.005,30, area,power)
    # path_t = circle_time(path_X,path_Y,0.015,t_start)
    
    # generate_heat_path(power, path_X, path_Y, path_t,path_Q)
    # generate_material_path(area, path_X, path_Y, path_t,path_A)
    
    # #BREAK
    # t_start = path_t[-1] + 1
    # heat_path.write(coord_string(t_start,0.007,0,7.3*10**(-3),power))
    # material_path.write(coord_string(t_start,0.007,0,7.3*10**(-3),area))
    
    # #THIRD CIRCLE
    # path_X,path_Y,path_A,path_Q = circle_path(0.007,300,area,power)
    # path_t = circle_time(path_X,path_Y,0.015,t_start)
    
    # generate_heat_path(power, path_X, path_Y, path_t,path_Q)
    # generate_material_path(area, path_X, path_Y, path_t,path_A)
    
main()