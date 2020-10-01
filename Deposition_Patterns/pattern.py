# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:33:09 2020

@author: Kari Ness
"""
#FUTURE IMPROVEMENTS:
#check valid length
#implement negative axis and possibility to do alternate ply-dir
#input 3 corners to span surface -> find normal for stack_dir
#start dir generated from two points
#number of layers instead of thickness
#flip stack dir
#make lenght and corner read-only

import abc #for abstract methods

#Creating a parent class for all deposition patterns
class Pattern:
  def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
    #initializing geometry properties
    self.thickness = thickness
    self.road_width = road_width
    self.length = [x_length, y_length,z_length]
    
    #initializing deposition velocity with default value 5
    self.v = 0.01
    
    #energy deposition
    self.P = P
    
    #initializing the start coorsinate of the pattern
    self.corner_coord = (corner_x, corner_y, corner_z)
    
    #initializing a dictionary with axes
    self.axis = {'deposition': 0, 'transverse': 1, 'stack': 2}
    

#Creating getters and setters
  @abc.abstractmethod
  def get_path(self):
      pass
  
  def generate_heat_path(self):
      path = self.get_path()
      
      #creating text files for heat and material path
      heat_path = open("heat_path.txt","w+")
      heat_path.truncate(0)  
      
      for elem in path:
          heat_path.write(self.coord_string(elem[0], elem[1], elem[2], elem[3], elem[4]))
          
  def generate_material_path(self):
      path = self.get_path()
      
      #creating text files for heat and material path
      material_path = open("material_path.txt","w+")
      material_path.truncate(0)  

      for elem in path:
          material_path.write(self.coord_string(elem[0], elem[1], elem[2], elem[3], elem[5]))

      
    
  def get_length(self):
      return self.length

  def get_z_length(self):
      return self.get_length()[2]
  
    
  def get_layer_nr(self):
      return int(self.get_length()[self.get_stack_dir()]/self.get_thickness())
        
  def get_thickness(self):
      return self.thickness
  
  def set_thickness(self, thickness):
      self.thickness = thickness
      
  def get_x_length(self):
      return self.get_length()[0]

  def get_y_length(self):
      return self.get_length()[1]
      
  def get_corner_coord(self):
      return self.corner_coord

  def get_road_width(self):
      return self.road_width
  
  def set_road_width(self, road_width):
      self.road_width = road_width   
      
  def get_axis(self):
      return self.axis
  
  def set_axis(self, deposition, transverse, stack):
      if (deposition == 0 or deposition == 1 or deposition == 2):
          self.axis['deposition'] = deposition
      else:
          raise ValueError("Invalid deposition axis!")
          
      if (transverse == 0 or transverse == 1 or transverse == 2) and (transverse != deposition):
          self.axis['transverse'] = transverse
      else:
          raise ValueError("Invalid deposition axis!")
          
      if (stack == 0 or stack == 1 or stack == 2) and (stack != deposition and stack != transverse):
          self.axis['stack'] = stack
      else:
          raise ValueError("Invalid deposition axis!")
      
  def get_stack_dir(self):
      return self.get_axis()['stack']   
      
  def get_deposition_dir(self):
      return self.get_axis()['deposition']
  
  def get_transverse_dir(self):
      return self.get_axis()['transverse']
          
  def get_power(self):
      return self.P
  
  def set_power(self, P):
      self.P = P
      
  def get_area(self):
      return self.get_road_width()*self.get_thickness()
  
  def get_velocity(self):
      return self.v
  
  def set_velocity(self,v):
      self.v = v
      
  def coord_string(self,t,x,y,z,p):
      temp= "{},{},{},{},{}\n"
      return temp.format(t,x,y,z,p)

    
