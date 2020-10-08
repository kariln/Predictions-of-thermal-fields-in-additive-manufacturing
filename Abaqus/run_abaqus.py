# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:01:35 2020

@author: Kari Ness
"""
import subprocess as sp
abaqus_path = "C:\\SIMULIA\\Commands\\abaqus.cmd"
script_path = "C:\\Users\\Kari Ness\\Documents\\GitHub\\TKT4550---Structural-Engineering-Specialization-Project\\Abaqus\\create_part.py"
sp.call([abaqus_path, 'cae', "noGUI=C:\\temp\\create_part.py"],shell = True)
