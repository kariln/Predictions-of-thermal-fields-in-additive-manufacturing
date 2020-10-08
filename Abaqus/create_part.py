# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 11:33:32 2020

@author: Kari Ness
BUILD ABAQUS GEOMETRY
"""
import os
clear = lambda: os.system('cls')  # On Windows System
clear()

#importing abaqus modules used in the script file
from part import *
from material import *
from section import * 
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

#paths
import sys
sys.path.append('C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials')
sys.path.append( 'C:\\Users\\Kari Ness\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )

from customKernel import *
from amModule import *

session.journalOptions.setValues(recoverGeometry=COORDINATE)


#create model
thermal = mdb.Model(name= 'Thermal')

"""PART"""
part1 = thermal.Part(dimensionality=THREE_D,name='Part_1', type = DEFORMABLE_BODY)
f, e = part1.faces, part1.edges #getting the edges and faces of part1

#extrude substrate
substrate_sketch = thermal.ConstrainedSketch(name='__profile__',sheetSize=2.0)
substrate_sketch.rectangle(point1=(-1.0,-1.0),point2=(1.0,1.0))
part1.BaseSolidExtrude(sketch=substrate_sketch,depth=0.5)
del thermal.sketches['__profile__']

#extrude AM
subs_top_plane = f.findAt(((0.7,0.7,500.E-03),))[0]
sketch_UpEdge_AM = e.findAt(((0.,1.0,500.E-03),))[0]
sketch_transform = part1.MakeSketchTransform(sketchPlane = subs_top_plane,sketchUpEdge=sketch_UpEdge_AM,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,origin=(0.0,0.0,0.5))
AM_sketch = thermal.ConstrainedSketch(name = '__profile__',sheetSize=2.0,gridSpacing=0.14, transform=sketch_transform)
AM_sketch.rectangle(point1=(-0.6,-0.6),point2=(0.6,0.6))
part1.SolidExtrude(depth=0.8,sketchPlane=subs_top_plane,sketchUpEdge=sketch_UpEdge_AM,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,sketch = AM_sketch,flipExtrudeDirection=OFF)
del thermal.sketches['__profile__']

#partition AM into layers
nr_layers = 4
plane_offset = 0.5
for i in range(0,nr_layers):
    datum_id = part1.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id
    plane = part1.datums[datum_id]
    plane_offset += 0.2
    part1_cells = part1.cells
    top_cell = part1_cells.findAt(((0.,0.,1.3),))
    part1.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)

"""PROPERTY"""
#Material
AA2319 = thermal.Material(name='AA2319')
conductivity_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_conductivity.txt")
conductivity_table = []
with open(conductivity_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        conductivity_table.append(tmp)
AA2319.Conductivity(temperatureDependency=ON,table=conductivity_table)

density_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_density.txt")
density_table = []
with open(density_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        density_table.append(tmp)
AA2319.Density(temperatureDependency=OFF,table=density_table)

elasticity_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_elasticity.txt")
elasticity_table = []
with open(elasticity_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        elasticity_table.append(tmp)
AA2319.Elastic(temperatureDependency=ON,table=elasticity_table)

expansion_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_expansion.txt")
expansion_table = []
with open(expansion_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        expansion_table.append(tmp)
AA2319.Expansion(temperatureDependency=ON,table=expansion_table)

latent_heat_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_latent_heat.txt")
latent_heat_table = []
with open(latent_heat_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        latent_heat_table.append(tmp)
AA2319.LatentHeat(table=latent_heat_table)

plasticity_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_plasticity.txt")
plasticity_table = []
with open(plasticity_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        plasticity_table.append(tmp)
AA2319.Plastic(temperatureDependency=ON,table=plasticity_table)

specific_heat_file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials", "AA2319_specific_heat.txt")
specific_heat_table = []
with open(specific_heat_file,"r") as file:
    for line in file:
        tmp = line.strip().split(",")
        for i in range(0,len(tmp)):
            tmp[i] = float(tmp[i])
        tmp = tuple(tmp)
        specific_heat_table.append(tmp)
AA2319.SpecificHeat(temperatureDependency=ON,table=specific_heat_table)

