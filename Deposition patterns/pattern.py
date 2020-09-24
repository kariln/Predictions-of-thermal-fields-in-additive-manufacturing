# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:33:09 2020

@author: Kari Ness
"""
#Creating a parent class for all deposition patterns
class Pattern:
  def __init__(self, z_length, thickness, x_length, y_length, start_x, start_y, start_z, road_width):
    #initializing geometry properties
    self.z_length = z_length
    self.thickness = thickness
    self.x_length = x_length
    self.y_length = y_length
    self.road_width = road_width
    
    #initializing the start coorsinate of the pattern
    self.start_coord = (start_x, start_y, start_z)
    
    #initializing the stack direction of the layers. default choice is z-direction.
    self.stack_dir = 2
    
    #initializing the starting deposition direction. default choice is x-direction
    self.start_dir = 0
    
    #initializing list for path coordinates
    self.path = [self.start_coord]
    

#Creating getters and setters
  def get_z_length(self):
      return self.z_length
  
  def set_z_length(self,z_length):
      self.z_length = z_length
        
    
  def get_layer_nr(self):
      if self.stack_dir == 0:
          return self.get_x_length/self.get_thickness
      elif self.stack_dir == 1:
          return self.get_x_length/self.get_thickness
      else:
          return self.get_z_length/self.get_thickness
        
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
      
  def get_start_coord(self):
      return self.start_coord
  
  def set_start_coord(self, x,y,z):
      self.start_coord = (x,y,z)

  def get_road_width(self):
      return self.road_width
  
  def set_road_width(self, road_width):
      self.road_width = road_width    
      
  def get_stack_dir(self):
      return self.stack_dir
  
  def set_stack_dir(self, stack_dir):
      if self.get_start_dir == stack_dir:
          raise ValueError("Start direction must be different from stack direction.")
      else:
          self.stack_dir = stack_dir    
      
  def get_start_dir(self):
      return self.start_dir
  
  def set_start_dir(self, start_dir):
      if start_dir == self.get_stack_dir:
          raise ValueError("Start direction must be different from stack direction.")
      else:
          self.start_dir = start_dir