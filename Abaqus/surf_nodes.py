# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:44:00 2021

@author: kariln
"""
part = mdb.models['thermal'].parts['part1']

surf_nodes = []
for face in part.elementFaces:
	if len(face.getElements()) == 1:
		surf_nodes.extend([node for node in face.getNodes() if node not in surf_nodes])
surf_file = open('surf_file.txt','w')
surf_file.write('x,y,z\n')
for elem in surf_nodes:      
    x = surf_nodes[0].coordinates[0]
    y = surf_nodes[0].coordinates[1]
    z = surf_nodes[0].coordinates[2]
    surf_file.write(str(x) + ',' + str(y) + ',' + str(z)+'\n')
surf_file.close()