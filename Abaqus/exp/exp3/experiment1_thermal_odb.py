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
import os
from os import *

odb = openOdb('experiment1_thermal.odb')

instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']

stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
add_elements = add_set.elements
nodes = []
for element in add_elements[0]:
	temp = element.connectivity
	for i in temp:
		if i not in nodes:
			nodes.append(i)

