# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by kariln on Wed Sep 16 10:21:14 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.34896, 1.35), width=198.567, 
    height=133.92)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execPyFile(
    'C:/SIMULIA/CAE/2019/win_b64/code/python2.7/lib/noGuiInteractive.pyc', 
    __main__.__dict__)
#: Model: C:/Users/kariln/Documents/GitHub/TKT4550---Structural-Engineering-Specialization-Project/Abaqus/Li's odb/Kari_thermal.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       8
#: Number of Node Sets:          9
#: Number of Steps:              2
