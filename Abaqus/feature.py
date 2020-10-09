# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:31:22 2020

@author: kariln
"""

class Feature:
    def __init__(self, feature_name, part, point1, point2, depth):
        self.feature_name = feature_name
        self.part = part
        self.point1 = point1
        self.point2 = point2
        self.depth = depth
        
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