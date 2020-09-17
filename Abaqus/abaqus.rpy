# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by Kari Ness on Tue Sep 15 13:58:23 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=92.2171783447266, 
    height=104.280563354492)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
import sys
sys.path.append(
    'c:\\Users\\Kari Ness\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )
from abaqus import *
from amConstants import *
import customKernel, amModule, amKernelInit
sys.path.append(
    'c:\\Users\\Kari Ness\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )
from customKernel import *
from amModule import *
install()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb(' one-layer disk.cae')
#: The model database "C:\Users\Kari Ness\Documents\GitHub\TKT4550---Structural-Engineering-Specialization-Project\Abaqus\ one-layer disk.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['thermal'].parts['thermal']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['thermal'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON, optimizationTasks=OFF, 
    geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.193757, 
    farPlane=0.401187, width=0.209716, height=0.0896742, cameraPosition=(
    0.204524, 0.200857, 0.18043), cameraUpVector=(-0.883094, 0.447325, 
    -0.141582))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.222191, 
    farPlane=0.378775, width=0.240492, height=0.102834, cameraPosition=(
    0.151032, -0.0600126, -0.249313), cameraUpVector=(0.26502, -0.635379, 
    0.725299), cameraTarget=(0.0327788, 0.0291117, 0.00868362))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.244817, 
    farPlane=0.354771, width=0.264981, height=0.113306, cameraPosition=(
    0.037257, 0.00474001, -0.288069), cameraUpVector=(-0.0611785, -0.909923, 
    0.410241), cameraTarget=(0.0316385, 0.0297607, 0.00829519))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.233795, 
    farPlane=0.365793, width=0.324115, height=0.138591, 
    viewOffsetX=0.000735637, viewOffsetY=-0.00010983)
p1 = mdb.models['thermal'].parts['thermal']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
p = mdb.models['thermal'].parts['thermal']
s = p.features['Solid extrude-1'].sketch
mdb.models['thermal'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['thermal'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s1.unsetPrimaryObject()
del mdb.models['thermal'].sketches['__edit__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.201059, 
    farPlane=0.395462, width=0.217619, height=0.0930537, cameraPosition=(
    0.0932056, 0.277613, -0.143255), cameraUpVector=(0.0136078, -0.78275, 
    -0.622188))
p = mdb.models['thermal'].parts['thermal']
s = p.features['Solid extrude-1'].sketch
mdb.models['thermal'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s2 = mdb.models['thermal'].sketches['__edit__']
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
s2.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s2, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s2.unsetPrimaryObject()
del mdb.models['thermal'].sketches['__edit__']
p = mdb.models['thermal'].parts['thermal']
s = p.features['Solid extrude-1'].sketch
mdb.models['thermal'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['thermal'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s1.unsetPrimaryObject()
del mdb.models['thermal'].sketches['__edit__']
p = mdb.models['thermal'].parts['thermal']
s = p.features['Solid extrude-1'].sketch
mdb.models['thermal'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s2 = mdb.models['thermal'].sketches['__edit__']
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
s2.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s2, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s2.unsetPrimaryObject()
del mdb.models['thermal'].sketches['__edit__']
p = mdb.models['thermal'].parts['thermal']
p.regenerate()
p = mdb.models['thermal'].parts['thermal']
s = p.features['Solid extrude-1'].sketch
mdb.models['thermal'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['thermal'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s1.unsetPrimaryObject()
del mdb.models['thermal'].sketches['__edit__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.232886, 
    farPlane=0.456578, width=0.252068, height=0.107784, cameraPosition=(
    0.208771, 0.275175, -0.0037047), cameraUpVector=(0.562197, -0.739826, 
    0.369584), cameraTarget=(0.0439853, 0.0288756, 0.0222165))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.250797, 
    farPlane=0.442967, width=0.271455, height=0.116074, cameraPosition=(
    0.0675341, 0.279782, 0.205907), cameraUpVector=(-0.241371, -0.742023, 
    0.625413), cameraTarget=(0.024623, 0.0295072, 0.0509524))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.241772, 
    farPlane=0.450766, width=0.261687, height=0.111897, cameraPosition=(
    0.0985719, 0.294306, 0.166252), cameraUpVector=(-0.222063, -0.652272, 
    0.724727), cameraTarget=(0.029044, 0.031576, 0.045304))
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.237217, 
    farPlane=0.455321, width=0.310393, height=0.132724, viewOffsetX=0.013439, 
    viewOffsetY=-0.00229116)
mdb.save()
#: The model database has been saved to "C:\Users\Kari Ness\Documents\GitHub\TKT4550---Structural-Engineering-Specialization-Project\Abaqus\ one-layer disk.cae".
