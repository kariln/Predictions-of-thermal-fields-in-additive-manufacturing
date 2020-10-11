import os
clear = lambda: os.system('cls')
clear()

#importing modulesfrom part import *
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
from customKernel import *
from amModule import *
session.journalOptions.setValues(recoverGeometry=COORDINATE)

#Include paths
import sys
sys.path.append(r'C:\Users\kariln\Documents\GitHub\Master\Materials')
sys.path.append(r'C:\Users\Kari Ness\abaqus_plugins\AM plugin\AMModeler\AMModeler')

#MODEL
thermal = mdb.Model(name= 'thermal')

#PART
part1=thermal.Part(dimensionality =THREE_D , name= 'part1' , type = DEFORMABLE_BODY)
f, e = part1.faces, part1.edges #getting the edges and faces of the part

#extrusion of base
sketch_name = thermal.ConstrainedSketch(name='__profile__',sheetSize= 8.0)
sketch_name.rectangle(point1=(-1.0, -1.0),point2=((1.0, 1.0)))
part1.BaseSolidExtrude(sketch=sketch_name,depth=0.5)
del thermal.sketches['__profile__']

substrate_top_plane = f.findAt(((0.0, 0.0, 0.5),))[0]
sketch_UpEdge = e.findAt(((0.0, 1.0, 0.5),))[0]
sketch_transform = part1.MakeSketchTransform(sketchPlane = substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,origin=(0.0,0.0,0.5))
AM_sketch = thermal.ConstrainedSketch(name = '__profile__',sheetSize=8.0,gridSpacing=0.14, transform=sketch_transform)
AM_sketch.rectangle(point1=(-0.6, -0.6),point2=(0.6, 0.6))
part1.SolidExtrude(depth=0.8,sketchPlane=substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,sketch = AM_sketch,flipExtrudeDirection=OFF)
del thermal.sketches['__profile__']

nr_layers = 4
plane_offset = 0.5
for i in range(0,nr_layers):
	datum_id = part1.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id
	plane = part1.datums[datum_id]
	plane_offset += 0.2
	part1_cells = part1.cells
	top_cell = part1_cells.findAt(((0.,0.,1.3),))
	part1.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)

