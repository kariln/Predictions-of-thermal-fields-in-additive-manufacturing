import os
clear = lambda: os.system('cls')
clear()
clear()

#importing modules
import abaqus
from abaqus import *
import abaqusConstants
from abaqusConstants import *
import odbAccess
from odbAccess import *

odb = openOdb('experiment20_thermal.odb')

part = mdb.models['thermal'].parts['part1']
instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
add_elements = add_set.elements[0]

stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
#GET TEMPERATURE
base_depth = 0.02
road_width = 0.005
layer_thickness = 0.0015
point1 = (-0.08, -0.06)
point2 = (0.08, 0.06)
new_active_nodes = -1
dispFile = open('disp.txt','w')
dispFile.write('i,t,T,x,y,z,t_i,T_1,T_2,T_3,T_4,T_5,pattern,road_width,v,basedepth,layer_thickness,globalseed,surface,nr_surf_nodes,layerNum\n')
surf_nodes = []
for face in part.elementFaces:
	if len(face.getElements()) == 1:
		surf_nodes.extend([node for node in face.getNodes() if node not in surf_nodes])
stepName = odb.steps.keys()[0]

frames = odb.steps[stepName].frames
active_elements = []
active_nodes = []
active_time = []
frame_index = -1
current_layer = 1
for frame in frames:
	frame_index += 1
	time = frame.frameValue
	if time > 2000:
		raise SystemExit(0)
	#find active elements for frame
	active = frame.fieldOutputs['EACTIVE'].values
	for i in range(0,len(active)):
		if active[i].data == 1.0 and active[i].elementLabel not in active_elements:
			active_elements.append(active[i].elementLabel)
			for element in add_elements:
				if element.label == active[i].elementLabel:
					temp = element.connectivity
					for j in temp:
						if j not in active_nodes:
							active_time.append(time)
							active_nodes.append(j)

	#checking if deposition has ended
	if new_active_nodes == len(active_nodes):
		pass
	else:
		new_active_nodes = len(active_nodes)
		temperature = frame.fieldOutputs['NT11']
		position = frame.fieldOutputs['COORD']
		if active_nodes != []:
			for i in range(0,len(temperature.values)):
				pos = position.values[i]
				temp = temperature.values[i]
				if temp.nodeLabel in active_nodes:
					hist_temp = [] #to store historical temperature values
					for k in range(1,6):
						if frame_index-k <1:
							hist_temp.append(None)
						else:
							tmp_frame = frames[frame_index-k] #fetching the frame k numbers behind the current frame
							tmp_temperature = tmp_frame.fieldOutputs['NT11']
							tmp_temp = tmp_temperature.values[i]
							print(temp.nodeLabel + tmp_temp.nodeLabel)
							hist_temp.append(tmp_temp.data)
					i = temp.nodeLabel
					t = time
					t_i = active_time[active_nodes.index(temp.nodeLabel)]
					T = temp.data
					x = pos.data[0]
					y = pos.data[1]
					z = pos.data[2]
					height = base_depth
					while z > height:
						height += layer_thickness
					layerNum = (height-base_depth)/layer_thickness
					if layerNum > current_layer:
						current_layer = layerNum
					nr_surf_nodes = 0 
					for elem in surf_nodes:
						if elem.label == i:
							surface = 1
						else:
							surface = 0
						if abs(elem.coordinates[0] - x) < 3*road_width and abs(elem.coordinates[1] - y) < 3*road_width and abs(elem.coordinates[2] - z) < 3*road_width:
							nr_surf_nodes += 1
						else:
							pass
					dispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(t_i) + ',' + str(hist_temp[0]) + ',' + str(hist_temp[1]) + ',' + str(hist_temp[2]) + ',' + str(hist_temp[3]) + ',' + str(hist_temp[4]) + ',zigzag,0.005,0.015,0.02,0.0015,0.005,' + str(surface)+',' + str(nr_surf_nodes)+',' + str(layerNum)+'\n')
dispFile.close()
