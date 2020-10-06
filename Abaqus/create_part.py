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

session.journalOptions.setValues(recoverGeometry=COORDINATE)

"""Create sketch and part """
#create model
thermal = mdb.Model(name= 'Thermal')

#create part
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
