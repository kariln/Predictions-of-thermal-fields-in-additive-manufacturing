
#importing modules
import abaqus
from abaqus import *
import abaqusConstants
from abaqusConstants import *
import odbAccess
from odbAccess import *

odb = openOdb('experiment2_thermal.odb')

part = mdb.models['thermal'].parts['part1']
instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
add_elements = add_set.elements[0]

stepName = odb.steps.keys()[0]

surf_nodes = []
for face in part.elementFaces:
	if len(face.getElements()) == 1:
		surf_nodes.extend([node for node in face.getNodes() if node not in surf_nodes])
surf_file = open('surf_file.txt','w')
surf_file.write('i,x,y,z\n')
for elem in surf_nodes:      
    i = elem.label
    x = elem.coordinates[0]
    y = elem.coordinates[1]
    z = elem.coordinates[2]
    surf_file.write(str(i) + ',' + str(x) + ',' + str(y) + ',' + str(z)+'\n')
surf_file.close()
dispFile = open('disp.txt','w')
dispFile.write('i,t,T,x,y,z,t_i,T_1,T_2,T_3,T_4,T_5,road_width,globalseed,v,basedepth,layer_thickness,layerNum,surface,nr_surf,pattern\n')
#GET TEMPERATURE
base_depth = 0.02
road_width = 0.005
layer_thickness = 0.0015
point1 = (-0.04, -0.04)
point2 = (0.04, 0.04)
new_active_nodes = -1
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
					dispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(t_i) + ',' + str(hist_temp[0]) + ',' + str(hist_temp[1]) + ',' + str(hist_temp[2]) + ',' + str(hist_temp[3]) + ',' + str(hist_temp[4]) + ',raster,0.01,0.015,0.02,0.0023,0.005,' + str(layerNum)+'\n')
dispFile.close()
