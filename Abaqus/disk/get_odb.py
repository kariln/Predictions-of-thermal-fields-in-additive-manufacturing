# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#
# Script to read data from odb file and save it to a csv file
#
from odbAccess import *
import sys

#Opens the odb
odb = openOdb('Job-1.odb')

#Access the steps in the odb
step1 = odb.steps['heat']

# Extracts a history output region for step1
historyRegions = step1.historyRegions
print(historyRegions)
# region = step1.historyRegions['Node corner-1.nn']
# temperatureData = region.historyOutputs['T'].data
# nn = len(temperatureData)
# dispFile = open('disp.csv','w')
# for i in range(0, nn):
#     dispFile.write('%10.4E,%10.4E \n’%(temperatureData[i][0], temperatureData[i][1])')
# dispFile.close()
