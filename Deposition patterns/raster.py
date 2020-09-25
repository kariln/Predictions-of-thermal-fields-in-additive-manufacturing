# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:39:34 2020

@author: Kari Ness
"""

import pattern
class Raster(pattern.Pattern):
    
    def __init__(self, layer_nr, thickness, width, height, start_x, start_y, start_z, road_width):
        super().__init__(self, layer_nr, thickness, width, height, start_x, start_y, start_z, road_width)
        
    def generate_path(self):
        
