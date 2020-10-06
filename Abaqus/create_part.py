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

sys.path.append( 'c:\\Users\\Kari Ness\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )
from customKernel import *
from amModule import *

"""Create sketch and part """
#create model
model1 = mdb.Model(name= 'Model_1')

#create part
part1 = model1.Part(dimensionality=THREE_D,name='Part_1', type = DEFORMABLE_BODY)

#extrude substrate
substrate_sketch = model1.ConstrainedSketch(name='__profile__',sheetSize=2.0)
substrate_sketch.rectangle(point1=(-1.0,-1.0),point2=(1.0,1.0))
part1.BaseSolidExtrude(sketch=substrate_sketch,depth=0.5)
del substrate_sketch


#extrude layers
layer_sketch=model1.ConstrainedSketch(name='__profile__',sheetSize=2.0)
layer_sketch.rectangle(point1=(-0.6, -0.6), 
    point2=(0.6, 0.6))
top_face = part1.faces.findAt(((0.0,0.0,1.4),))
sketch_UpEdge = part1.edges.findAt(((0.6,0.6,1.1),))
part1.SolidExtrude(depth=0.8, 
    flipExtrudeDirection=OFF, sketch=
    layer_sketch, sketchOrientation=RIGHT, 
    sketchPlane=top_face, 
    sketchPlaneSide=SIDE1, sketchUpEdge=
    sketch_UpEdge)
del layer_sketch