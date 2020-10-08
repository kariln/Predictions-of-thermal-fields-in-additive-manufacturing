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
class Material:
    def __init__(self,material_properties, material_name):
        #The material_properties should be a list of strings containing material property types
        self.material_properties = material_properties
        
        #The material should be a string
        self.material_name = material_name
        
    def get_material_name(self):
        return self.material_name
        
    def get_property_file(self, material_property):
        file_name = self.get_material_name() + '_' + material_property + '.txt'
        file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), file_name)
        return file
    
    def get_property_table(self, material_property):
        file = self.get_property_file(material_property)
        table = []
        with open(file,"r") as f:
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table
    
AA2319 = thermal.Material(name='AA2319')
AA2319_object = Material(['conductivity','density','elasticity','expansion','latent_heat','plasticity','specific_heat'],'AA2319')
property_table = AA2319_object.get_property_table('conductivity')
AA2319.Conductivity(temperatureDependency=ON,table=property_table)
AA2319.Density(temperatureDependency=OFF,table=density_table)
AA2319.Elastic(temperatureDependency=ON,table=elasticity_table)
AA2319.Expansion(temperatureDependency=ON,table=expansion_table)
AA2319.LatentHeat(table=latent_heat_table)
AA2319.Plastic(temperatureDependency=ON,table=plasticity_table)
AA2319.SpecificHeat(temperatureDependency=ON,table=specific_heat_table)

