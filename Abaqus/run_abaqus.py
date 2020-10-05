# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:01:35 2020

@author: Kari Ness
"""
import create_part
abaqusPath = "C:\\SIMULIA\\Commands\\abaqus.cmd /C"
args = abaqusPath + "abaqus python test.py"
create_part.call(args)