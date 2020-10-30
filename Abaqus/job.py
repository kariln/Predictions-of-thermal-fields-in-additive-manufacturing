# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:51:24 2020

@author: kariln
"""

class Job:
    def __init__(self,job_name, model_name):
        self.job_name = job_name 
        self.model_name = model_name
        
    def get_job_name(self):
        return self.job_name
        
    def get_model_name(self):
        return self.model_name
    