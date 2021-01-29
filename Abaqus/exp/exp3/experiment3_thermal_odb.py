# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:07:22 2021

@author: Kari Ness
"""

import os
clear = lambda: os.system('cls')
clear()

#importing modules
import abaqus
from abaqus import *
import abaqusConstants
from abaqusConstants import *
import odbAccess
from odbAccess import *

odb = openOdb('experiment1_thermal.odb')

instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
add_elements = add_set.elements[0]

stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
add_elements = add_set.elements[0]

#GET TEMPERATURE
base_depth = 0.02
dispFile = open('disp.txt','w')
dispFile.write('i,t,T,x,y,z,Q_x,Q_y_,Q_z\n')
stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
for frame in frames:
	time = frame.frameValue
	if time > 2000:
		raise SystemExit(0)
#find active elements for frame
	active = frame.fieldOutputs['EACTIVE'].values
	active_elements = []
	active_nodes = []
	for i in range(0,len(active)):
		if active[i].data == 1.0:
			active_elements.append(active[i].elementLabel)
			for element in add_elements:
				if element.label in active_elements:
					temp = element.connectivity
					for i in temp:
						if i not in active_nodes:
							active_nodes.append(i)

	temperature = frame.fieldOutputs['NT11']
	position = frame.fieldOutputs['COORD']
#get laser position for frame
	last_nodes_labels = active_nodes[-4::]
	last_nodes_x = []
	last_nodes_y = []
	last_nodes_z = []
	for j in reversed(range(0,len(position.values))):
		pos = position.values[j]
		if pos.nodeLabel in last_nodes_labels:
			x = pos.data[0]
			y = pos.data[1]
			z = pos.data[2]
			last_nodes_x.append(x)
			last_nodes_y.append(y)
			last_nodes_z.append(z)
			if len(last_nodes_x) == 4:
				break
	if active_nodes != []:
		Q_z = max(last_nodes_z)
		Q_x = sum(last_nodes_x) / len(last_nodes_x)
		Q_y = sum(last_nodes_y) / len(last_nodes_y)
#get laser position for frame
	last_nodes_labels = active_nodes[-4::]
	last_nodes_x = []
	last_nodes_y = []
	last_nodes_z = []
	for j in reversed(range(0,len(position.values))):
		pos = position.values[j]
		if pos.nodeLabel in last_nodes_labels:
			x = pos.data[0]
			y = pos.data[1]
			z = pos.data[2]
			last_nodes_x.append(x)
			last_nodes_y.append(y)
			last_nodes_z.append(z)
			if len(last_nodes_x) == 4:
				break
	if active_nodes != []:
		Q_z = max(last_nodes_z)
		Q_x = sum(last_nodes_x) / len(last_nodes_x)
		Q_y = sum(last_nodes_y) / len(last_nodes_y)
	for i in range(0,len(temperature.values)):
		pos = position.values[i]
		temp = temperature.values[i]
		if temp.nodeLabel in active_nodes:
			i = temp.nodeLabel
			t = time
			T = temp.data
			x = pos.data[0]
			y = pos.data[1]
			z = pos.data[2]
			dispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(Q_x) + ',' + str(Q_y) + ',' + str(Q_z) + '\n')
dispFile.close()