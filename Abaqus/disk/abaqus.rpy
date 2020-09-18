# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by kariln on Fri Sep 18 13:57:12 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=194.519790649414, 
    height=239.220016479492)
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
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
#* *** Error: File open failed (utl_File: CreateFile in OpenUpdate)
#* error: The process cannot access the file because it is being used by 
#* another process.
#* 
#* file: C:\Users\kariln\Documents\GitHub\TKT4550\Abaqus\disk\one-layer disk.cae
