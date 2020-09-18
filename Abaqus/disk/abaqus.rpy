# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by kariln on Thu Sep 17 19:05:07 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=193.980209350586, 
    height=236.790008544922)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
import sys
sys.path.append(
    'c:\\Users\\kariln\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )
from abaqus import *
from amConstants import *
import customKernel, amModule, amKernelInit
sys.path.append(
    'c:\\Users\\kariln\\abaqus_plugins\\AM plugin\\AMModeler\\AMModeler' )
from customKernel import *
from amModule import *
install()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('one-layer disk.cae')
#: The model database "C:\Users\kariln\Documents\GitHub\TKT4550\Abaqus\disk\one-layer disk.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['thermal'].parts['thermal']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
import sys
sys.path.insert(15, 
    r'c:/Users/kariln/abaqus_plugins/AM plugin/AMModeler/AMModeler')
from abaqus import *
from amConstants import *
import customKernel, amModule, amKernelInit
mdb.customData.am.amModels['AM-Model-1'].addEventSeries(
    eventSeriesName='material path', 
    eventSeriesTypeName='"ABQ_AM.MaterialDeposition"', timeSpan='TOTAL TIME', 
    fileName='C:/Users/kariln/Documents/GitHub/TKT4550/Abaqus/disk/material_input.txt', 
    isFile=ON)
mdb.customData.am.amModels['AM-Model-1'].dataSetup.eventSeries.changeKey(
    fromName='heat pathj', toName='heat path')
mdb.customData.am.amModels['AM-Model-1'].addEventSeries(
    eventSeriesName='heat path', 
    eventSeriesTypeName='"ABQ_AM.MaterialDeposition"', timeSpan='TOTAL TIME', 
    fileName='C:/temp/Master/One-layer disk/heat_input.txt', isFile=ON)
a = mdb.models['thermal'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
mdb.jobs['Job-1'].setValues(numCpus=1)
mdb.save()
#: The model database has been saved to "C:\Users\kariln\Documents\GitHub\TKT4550\Abaqus\disk\one-layer disk.cae".
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Error in job Job-1: EVENT SERIES heat pathj HAS NOT BEEN DEFINED.
#: Error in job Job-1: EVENT SERIES heat pathj HAS NOT BEEN DEFINED.
#: Error in job Job-1: EVENT SERIES heat pathj HAS NOT BEEN DEFINED.
#: Error in job Job-1: THE ANALYSIS HAS TERMINATED DUE TO PREVIOUS ERRORS.
#: Job Job-1: Abaqus/Standard aborted due to errors.
#: Error in job Job-1: Abaqus/Standard Analysis exited with an error - Please see the  message file for possible error messages if the file exists.
#: Job Job-1 aborted due to errors.
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
unhighlight(mdb.models['thermal'].rootAssembly.instances['thermal-1'])
highlight(mdb.models['thermal'].rootAssembly.instances['thermal-1'])
unhighlight(mdb.models['thermal'].rootAssembly.instances['thermal-1'])
mdb.customData.am.amModels['AM-Model-1'].dataSetup.eventSeries.changeKey(
    fromName='heat path', toName='heat pathj')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.save()
#: The model database has been saved to "C:\Users\kariln\Documents\GitHub\TKT4550\Abaqus\disk\one-layer disk.cae".
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
o3 = session.openOdb(
    name='C:/Users/kariln/Documents/GitHub/TKT4550/Abaqus/disk/Job-1.odb')
#: Model: C:/Users/kariln/Documents/GitHub/TKT4550/Abaqus/disk/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       6
#: Number of Node Sets:          5
#: Number of Steps:              2
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.214851, 
    farPlane=0.378423, width=0.193922, height=0.0992479, cameraPosition=(
    0.204227, 0.200616, 0.179521), cameraUpVector=(0.366939, -0.0141515, 
    -0.930137), cameraTarget=(0.0327724, 0.0291614, 0.00806624))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.221389, 
    farPlane=0.376215, width=0.199823, height=0.102268, cameraPosition=(
    0.151584, 0.231426, -0.173646), cameraUpVector=(-0.210495, -0.830294, 
    -0.516046), cameraTarget=(0.0328312, 0.029127, 0.00846054))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.226882, 
    farPlane=0.374571, width=0.204781, height=0.104806, cameraPosition=(
    0.288827, 0.0779928, -0.134849), cameraUpVector=(-0.721565, -0.200706, 
    -0.662617), cameraTarget=(0.0336736, 0.0281852, 0.00869869))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.211018, 
    farPlane=0.387608, width=0.190462, height=0.0974777, cameraPosition=(
    0.227244, 0.234892, 0.103884), cameraUpVector=(0.12373, -0.159896, 
    -0.979349), cameraTarget=(0.0329039, 0.0301461, 0.0116824))
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.220535, 
    farPlane=0.376433, width=0.199053, height=0.101874, cameraPosition=(
    0.137927, 0.253713, -0.154956), cameraUpVector=(-0.0402148, -0.831862, 
    -0.553523), cameraTarget=(0.0322042, 0.0302936, 0.00965453))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='TEMP', outputPosition=INTEGRATION_POINT, )
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
mdb.customData.am.amModels['AM-Model-1'].plotEventSeriesToViewPort(
    eventSeriesName='material path', fieldNum=0, timeStart=0, timeEnd=3, 
    isFitView=ON, showMinValEvents=ON)
#: 
#: Event Series plot info:
#: ---------------------------
#: Event Start -> time = 0.0,at ( 0.0,0.05,0.020575 ), value = 0.00023
#: End of Event -> time = 3, at ( 0.06,0.01,0.020575 ), value = 0.00023
mdb.customData.am.amModels['AM-Model-1'].plotEventSeriesToViewPort(
    eventSeriesName='material path', fieldNum=0, timeStart=0, timeEnd=3, 
    isFitView=OFF, showMinValEvents=ON)
#: 
#: Event Series plot info:
#: ---------------------------
#: Event Start -> time = 0.0,at ( 0.0,0.05,0.020575 ), value = 0.00023
#: End of Event -> time = 3, at ( 0.06,0.01,0.020575 ), value = 0.00023
vp=session.viewports[session.currentViewportName]
vp.assemblyDisplay.meshOptions.setValues(meshVisibleEdges=EXTERIOR)
vp.assemblyDisplay.setValues(renderStyle=SHADED)
