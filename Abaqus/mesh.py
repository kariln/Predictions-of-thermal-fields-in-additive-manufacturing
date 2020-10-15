# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:14:47 2020

@author: Kari Ness
"""

class Mesh:
    def __init__(self, part, global_seed):
        self.part = part
        self.global_seed = global_seed
        
    def get_global_seed(self):
        return self.global_seed