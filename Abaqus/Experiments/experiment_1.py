import os
clear = lambda: os.system('cls')
clear()

#importing modulesimport part
from part import *
import material
from material import *
import section
from section import *
import assembly
from assembly import *
import step
from step import *
import interaction
from interaction import *
import load
from load import *
import mesh
from mesh import *
import job
from job import *
import sketch
from sketch import *
import visualization
from visualization import *
import connectorBehavior
from connectorBehavior import *
import customKernel
from customKernel import *
import amModule
from amModule import *
import amKernelInit
from amKernelInit import *
import amConstants
from amConstants import *
import copy
from copy import *
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

#Include paths
import sys
sys.path.append(r'C:\Users\kariln\Documents\abagus_plugins\AM plugin\AMModeler\AMModeler')

#MODEL
thermal = mdb.Model(name= 'thermal')
mdb.models['thermal'].setValues(absoluteZero=-273.15, stefanBoltzmann=5.67E-08)

#PART
part1=thermal.Part(dimensionality =THREE_D , name= 'part1' , type = DEFORMABLE_BODY)
f, e = part1.faces, part1.edges #getting the edges and faces of the part

#extrusion of base
sketch_name = thermal.ConstrainedSketch(name='__profile__',sheetSize= 0.08000000000000002)
sketch_name.rectangle(point1=(-0.1, -0.1),point2=((0.1, 0.1)))
part1.BaseSolidExtrude(sketch=sketch_name,depth=0.02)
e = part1.edges
del thermal.sketches['__profile__']

substrate_top_plane = f.findAt(((0.0, 0.0, 0.02),))[0]
sketch_UpEdge = e.findAt(((0.0, 0.1, 0.02),))[0]
sketch_transform = part1.MakeSketchTransform(sketchPlane = substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,origin=(0.0,0.0,0.02))
AM_sketch = thermal.ConstrainedSketch(name = '__profile__',sheetSize=0.08000000000000002,gridSpacing=0.14, transform=sketch_transform)
AM_sketch.rectangle(point1=(-0.06, -0.06),point2=(0.06, 0.06))
part1.SolidExtrude(depth=0.0092,sketchPlane=substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,sketch = AM_sketch,flipExtrudeDirection=OFF)
del thermal.sketches['__profile__']
#partition AM into layers
nr_layers = 4
plane_offset = 0.02
for i in range(0,nr_layers):
	datum_id = part1.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id
	plane = part1.datums[datum_id]
	plane_offset += 0.0023
	part1_cells = part1.cells
	top_cell = part1_cells.findAt(((0.,0.,0.0292),))
	part1.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)

#PROPERTY
AA2319 = thermal.Material(name='AA2319')
