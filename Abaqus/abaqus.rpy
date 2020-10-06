# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by Kari Ness on Tue Oct  6 09:53:15 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.20703, 1.20139), width=177.675, 
    height=119.178)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('create_part.py', __main__.__dict__)
#: The model "Model_1" has been created.
#: Warning: findAt could not find a geometric entity at (0.0, 0.0, 1.4)
#: Warning: findAt could not find a geometric entity at (0.6, 0.6, 1.1)
#* Invalid sketch plane
#* File "create_part.py", line 55, in <module>
#*     sketch_UpEdge)
