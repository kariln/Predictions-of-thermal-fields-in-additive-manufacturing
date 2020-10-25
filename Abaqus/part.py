# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:32:49 2020

@author: kariln
"""
from feature import Feature
from mesh import Mesh
from sets import Set

class Part:
    def __init__(self, part_name, model, dimensionality, part_type):
        self.part_name = part_name
        self.model = model
        self.dimensionality = dimensionality
        self.part_type = part_type
        self.features = {}
        self.mesh = None
        self.sets = {}
        self.amModels = {}
        
    def get_dimensionality(self):
        return self.dimensionality
    
    def get_model(self):
        return self.model
    
    def get_model_name(self):
        model = self.get_model()
        return model.get_model_name()
    
    def get_part_name(self):
        return self.part_name
    
    def get_part_type(self):
        return self.part_type
    
    
    def get_features(self):
        return self.features
    
    def add_feature(self,feature):
        feature_name = feature.get_feature_name()
        self.get_features().update({feature_name:feature})
        
    def create_mesh(self,mesh):
        self.mesh = mesh
        
    def get_mesh(self):
        return self.mesh
    
    def get_sets(self):
        return self.sets
    
    def add_set(self,sett):
        set_name = sett.get_set_name()
        self.get_sets().update({set_name:sett})
        
    def get_amModels(self):
        return self.amModels
        
    def add_amModel(self,amModel):
        amModel_name = amModel.get_amModel_name()
        self.get_amModels().update({amModel_name:amModel})