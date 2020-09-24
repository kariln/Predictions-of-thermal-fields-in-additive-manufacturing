# -*- coding: utf-8 -*-
"""
Reading temperatures from Li's odb
"""
#PYTHON POST PROCESSING SCRIPT
#Run using python

#Packages
from abapy.misc import load
#import matplotlib.pyplot as plt
#import numpy as np

#Setting up paths
workdir = 'Li''s odb'
name = 'Kari_thermal.odb'

#Getting raw data
data = load(workdir + '/' + name + '.pckl')
print(data)

#Post processing
#ref_node_label = data['ref_node_label']
