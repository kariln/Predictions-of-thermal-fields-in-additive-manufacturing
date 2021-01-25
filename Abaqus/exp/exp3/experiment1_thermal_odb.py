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

stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
#GET TEMPERATURE
base_depth = 0.02
dispFile = open('disp.txt','w')
dispFile.write('i,t,T,x,y,z\n')
stepName = odb.steps.keys()[0]
#få inn eactive?
frames = odb.steps[stepName].frames
for frame in frames:
	time = frame.frameValue
	temperature = frame.fieldOutputs['NT11']
	position = frame.fieldOutputs['COORD']
	for i in range(0,len(temperature.values)):
		pos = position.values[i]
		if pos.data[2] > base_depth:
			temp = temperature.values[i]
			i = temp.nodeLabel
			t = time
			T = temp.data
			x = pos.data[0]
			y = pos.data[1]
			z = pos.data[2]
			if T != 20.0:
				dispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + '\n')
dispFile.close()
