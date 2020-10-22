# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:31:22 2020

@author: kariln
"""

class Feature:
    def __init__(self, part, point1, point2, depth, nr_layers):
        self.feature_name = None
        self.part = part
        self.point1 = point1
        self.point2 = point2
        self.depth = depth
        self.nr_layers = nr_layers
        self.layer_thickness = depth/nr_layers
        
    def get_feature_name(self):
        return self.feature_name
    
    def get_part(self):
        return self.part
    
    def get_depth(self):
        return self.depth
    
    def get_point1(self):
        return self.point1
    
    def get_point2(self):
        return self.point2
    
    def get_layers(self):
        return self.nr_layers
    
    def get_layer_thickness(self):
        return self.layer_thickness
    
    def get_side_length(self):
        return abs(self.get_point2()[0] - self.get_point1()[0])
    
    def set_feature_name(self,feature_name):
        self.feature_name = feature_name