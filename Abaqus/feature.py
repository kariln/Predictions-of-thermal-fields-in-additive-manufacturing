# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:31:22 2020

@author: kariln
"""

class Feature:
    def __init__(self, feature_name, part, depth):
        self.feature_name = feature_name
        self.part = part
        
    def get_feature_name(self):
        return self.feature_name
    
    def get_part(self):
        return self.part
    
    def get_depth(self):
        return self.depth