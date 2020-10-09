# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:29:24 2020

@author: kariln
"""
from part import Part

class Model:
    def __init__(self,model_name):
        self.model_name = model_name
        self.parts = {}
    
    def get_model_name(self):
        return self.model_name
    
    def get_parts(self):
        return self.parts
    
    def add_part(self,part):
        part_name = part.get_part_name()
        self.get_parts().update({part_name:part})