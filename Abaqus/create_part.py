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

"""Create sketch and part """
#substrate
mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=2.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-1.0,-1.0),point2=(1.0,1.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D,name='Part-1', type = DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(sketch=mdb.models['Model-1'].sketches['__profile__'],depth=0.5)
del mdb.models['Model-1'].sketches['__profile__']


#layers
mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=2.0)
sketch1 = mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-0.6, -0.6), 
    point2=(0.6, 0.6))
print(sketch_plane = mdb.models['Model-1'].parts['Part-1'].faces[4])
#mdb.models['Model-1'].parts['Part-1'].SolidExtrude(depth=0.8, 
#    flipExtrudeDirection=OFF, sketch=sketch1, sketchOrientation=RIGHT, 
#    sketchPlane=sketch_plane, 
#    sketchPlaneSide=SIDE1, sketchUpEdge=
#    mdb.models['Model-1'].parts['Part-1'].edges[7])
#del mdb.models['Model-1'].sketches['__profile__']