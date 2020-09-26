# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:33:09 2020

@author: Kari Ness
"""
#FUTURE IMPROVEMENTS:
#check valid length, axis
#implement negative axis and possibility to do alternate ply-dir
#input 3 corners to span surface -> find normal for stack_dir
#start dir generated from two points
#number of layers instead of thickness
#flip stack dir
#finish get print start
#map to local coordinate system

#Creating a parent class for all deposition patterns
class Pattern:
  def __init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
    #initializing geometry properties
    self.z_length = z_length
    self.thickness = thickness
    self.x_length = x_length
    self.y_length = y_length
    self.road_width = road_width
    
    #initializing deposition velocity with default value 5
    self.v = 5
    
    #energy deposition
    self.P = P
    
    #initializing the start coorsinate of the pattern
    self.corner_coord = (corner_x, corner_y, corner_z)
    
    #initializing the stack direction of the layers. default choice is z-direction.
    self.stack_dir = 3
    
    #initializing the starting deposition direction. default choice is x-direction
    self.start_dir = 1
    

#Creating getters and setters
  def get_z_length(self):
      return self.z_length
  
  def set_z_length(self,z_length):
      self.z_length = z_length
        
    
  def get_layer_nr(self):
      if self.stack_dir == 0:
          return self.get_x_length()/self.get_thickness()
      elif self.stack_dir == 1:
          return self.get_x_length()/self.get_thickness()
      else:
          return self.get_z_length()/self.get_thickness()
        
  def get_thickness(self):
      return self.thickness
  
  def set_thickness(self, thickness):
      self.thickness = thickness
      
  def get_x_length(self):
      return self.x_length
  
  def set_x_length(self, x_length):
      self.x_length = x_length
      
  def get_y_length(self):
      return self.y_length
  
  def set_y_length(self, y_length):
      self.y_length = y_length
      
  def get_corner_coord(self):
      return self.corner_coord
  
  def set_corner_coord(self, x,y,z):
      self.corner_coord = (x,y,z)

  def get_road_width(self):
      return self.road_width
  
  def set_road_width(self, road_width):
      self.road_width = road_width    
      
  def get_stack_dir(self):
      return self.stack_dir
  
  def set_stack_dir(self, stack_dir):
      if self.get_start_dir == stack_dir:
          raise ValueError("Start direction must be different from stack direction.")
          
      elif stack_dir not in {1,2,3}:
          raise ValueError("Stack direction must be a value of 1 (x), 2 (y) or 3 (z).")
          
      else:
          self.stack_dir = stack_dir    
      
  def get_start_dir(self):
      return self.start_dir
  
  def set_start_dir(self, start_dir):
      if start_dir == self.get_stack_dir:
          raise ValueError("Start direction must be different from stack direction.")
          
      elif start_dir not in {1,2,3}:
          raise ValueError("Start direction must be a value of 1 (x), 2 (y) or 3 (z).")
          
      else:
          self.start_dir = start_dir
          
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
      return '%(t),%(x),%(y),%(z),%(p)' % {"t": t, "x": x, "y" : y, "z": z, "p": p }
  

    
