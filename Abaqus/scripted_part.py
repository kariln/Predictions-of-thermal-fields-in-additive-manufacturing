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

