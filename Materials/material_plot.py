# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 19:41:40 2020

@author: Kari Ness
Plotting material properties and presenting them in a table
"""

class Material:
    def __init__(self,E, lambda, cp, alpha, sigma, k, h):
        #material parameters:
        self.E = E #Young's modulus
        self.lambda = lambda #thermal conductivity
        self.cp = cp #specific heat
        self.alpha = alpha #thermal expansion coefficient
        self.sigma = sigma #yield strength
        self.k = k #emissivity for air
        self.h = h #convection coefficient
        
        #perhaps strain hardening?
        
        
        