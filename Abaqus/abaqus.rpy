# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by kariln on Thu Oct  8 14:00:02 2020
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
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
#: (120.0, 3.39)
#: (121.0, 6.79)
#: (121.0, 10.2)
#: (122.0, 13.6)
#: (123.0, 17.0)
#: (123.0, 20.4)
#: (124.0, 23.8)
#: (125.0, 27.1)
#: (125.0, 30.5)
#: (126.0, 33.9)
#: (127.0, 37.3)
#: (127.0, 40.7)
#: (128.0, 44.1)
#: (128.0, 47.5)
#: (129.0, 50.9)
#: (129.0, 54.3)
#: (130.0, 57.7)
#: (131.0, 61.1)
#: (132.0, 64.5)
#: (133.0, 67.9)
#: (133.0, 71.3)
#: (134.0, 74.7)
#: (134.0, 78.1)
#: (135.0, 81.4)
#: (136.0, 84.8)
#: (137.0, 88.2)
#: (138.0, 91.6)
#: (138.0, 95.0)
#: (139.0, 98.4)
#: (140.0, 102.0)
#: (140.0, 105.0)
#: (140.0, 109.0)
#: (141.0, 112.0)
#: (142.0, 115.0)
#: (143.0, 119.0)
#: (144.0, 122.0)
#: (144.0, 126.0)
#: (145.0, 129.0)
#: (146.0, 132.0)
#: (146.0, 136.0)
#: (147.0, 139.0)
#: (148.0, 143.0)
#: (149.0, 146.0)
#: (149.0, 149.0)
#: (150.0, 153.0)
#: (150.0, 156.0)
#: (151.0, 160.0)
#: (151.0, 163.0)
#: (152.0, 166.0)
#: (152.0, 170.0)
#: (153.0, 173.0)
#: (153.0, 176.0)
#: (153.0, 180.0)
#: (153.0, 183.0)
#: (153.0, 187.0)
#: (154.0, 190.0)
#: (155.0, 193.0)
#: (155.0, 197.0)
#: (156.0, 204.0)
#: (156.0, 207.0)
#: (156.0, 210.0)
#: (156.0, 214.0)
#: (156.0, 217.0)
#: (157.0, 221.0)
#: (157.0, 224.0)
#: (157.0, 227.0)
#: (157.0, 231.0)
#: (158.0, 238.0)
#: (158.0, 241.0)
#: (158.0, 244.0)
#: (158.0, 251.0)
#: (158.0, 255.0)
#: (157.0, 261.0)
#: (157.0, 265.0)
#: (157.0, 268.0)
#: (157.0, 275.0)
#: (156.0, 278.0)
#: (156.0, 282.0)
#: (156.0, 288.0)
#: (156.0, 295.0)
#: (155.0, 299.0)
#: (155.0, 305.0)
#: (154.0, 309.0)
#: (154.0, 312.0)
#: (153.0, 316.0)
#: (153.0, 319.0)
#: (153.0, 322.0)
#: (153.0, 326.0)
#: (152.0, 329.0)
#: (152.0, 336.0)
#: (151.0, 339.0)
#: (151.0, 343.0)
#: (150.0, 350.0)
#: (149.0, 356.0)
#: (148.0, 360.0)
#: (148.0, 367.0)
#: (147.0, 373.0)
#: (146.0, 377.0)
#: (146.0, 383.0)
#: (145.0, 390.0)
#: (144.0, 397.0)
#: (144.0, 404.0)
#: (144.0, 407.0)
#: (144.0, 411.0)
#: (144.0, 417.0)
#: (144.0, 424.0)
#: (144.0, 431.0)
#: (144.0, 438.0)
#: (144.0, 445.0)
#: (144.0, 455.0)
#: (144.0, 462.0)
#: (144.0, 468.0)
#: (144.0, 475.0)
#: (144.0, 485.0)
#: (144.0, 492.0)
#: (144.0, 495.0)
#: (144.0, 499.0)
#: (144.0, 506.0)
#: (144.0, 516.0)
#: (144.0, 519.0)
#: (144.0, 526.0)
#: (144.0, 529.0)
#: (144.0, 540.0)
#: (144.0, 546.0)
#: (144.0, 550.0)
#: (146.0, 553.0)
#: (148.0, 557.0)
#: (154.0, 560.0)
#: (158.0, 563.0)
#: (167.0, 570.0)
#: (172.0, 574.0)
#: (176.0, 577.0)
#: (180.0, 580.0)
#: (184.0, 584.0)
#: (188.0, 587.0)
#: (192.0, 590.0)
#: (196.0, 594.0)
#: (196.0, 597.0)
#: (204.0, 601.0)
#: (205.0, 604.0)
#: (208.0, 607.0)
#: (213.0, 611.0)
#: (214.0, 614.0)
#: (219.0, 618.0)
#: (222.0, 621.0)
#: (226.0, 624.0)
#: (229.0, 628.0)
#: (233.0, 631.0)
#: (236.0, 635.0)
#: (239.0, 638.0)
#: (243.0, 641.0)
#: (247.0, 645.0)
#: (249.0, 648.0)
#: (253.0, 652.0)
#: (257.0, 655.0)
#: (260.0, 658.0)
#: (266.0, 665.0)
#: (269.0, 669.0)
#: (272.0, 672.0)
#: (277.0, 675.0)
#: (279.0, 679.0)
#: (284.0, 682.0)
#: (287.0, 686.0)
#: (291.0, 689.0)
#: (294.0, 692.0)
#: (294.0, 696.0)
#: (299.0, 699.0)
#: (300.0, 702.0)
#: (300.0, 706.0)
#: (300.0, 709.0)
#: (300.0, 713.0)
#: (300.0, 716.0)
#: (300.0, 723.0)
#: (300.0, 730.0)
#: (300.0, 743.0)
#: (300.0, 753.0)
#: (300.0, 760.0)
#: (300.0, 770.0)
#: (300.0, 787.0)
#: (300.0, 808.0)
#: (300.0, 821.0)
#: (300.0, 835.0)
#: (300.0, 842.0)
#: (300.0, 848.0)
#: (300.0, 852.0)
#: (300.0, 862.0)
#: (300.0, 865.0)
#: (300.0, 872.0)
#: (300.0, 882.0)
#: (300.0, 889.0)
#: (300.0, 899.0)
#: (300.0, 910.0)
#: (300.0, 920.0)
#: (300.0, 930.0)
#: (300.0, 940.0)
#: (300.0, 950.0)
#: (300.0, 964.0)
#: (300.0, 974.0)
#: (300.0, 984.0)
#: (300.0, 994.0)
#: (300.0, 1000.0)
#: (300.0, 1010.0)
#: (300.0, 1020.0)
#: (300.0, 1030.0)
#: (300.0, 1040.0)
#: (300.0, 1050.0)
#: (300.0, 1060.0)
#: (300.0, 1070.0)
#: (300.0, 1080.0)
#: (300.0, 1090.0)
#: (300.0, 1100.0)
#: (300.0, 1110.0)
#: (300.0, 1120.0)
#: (300.0, 1130.0)
#: (300.0, 1140.0)
#: (300.0, 1150.0)
#: (300.0, 1160.0)
#: (300.0, 1170.0)
#: (300.0, 1180.0)
#: (300.0, 1190.0)
#: (300.0, 1200.0)
#: (300.0, 1210.0)
#: (300.0, 1220.0)
#: (300.0, 1230.0)
#: (300.0, 1240.0)
#: (300.0, 1250.0)
#: (300.0, 1270.0)
#: (300.0, 1280.0)
#: (300.0, 1290.0)
#: (300.0, 1300.0)
#: (300.0, 1310.0)
#: (300.0, 1320.0)
#: (300.0, 1330.0)
#: (300.0, 1340.0)
#: (300.0, 1350.0)
#: (300.0, 1360.0)
#: (300.0, 1370.0)
#: (300.0, 1380.0)
#: (300.0, 1390.0)
#: (300.0, 1400.0)
#: (300.0, 1410.0)
#: (300.0, 1420.0)
#: (300.0, 1430.0)
#: (300.0, 1440.0)
#: (300.0, 1460.0)
#: (300.0, 1470.0)
#: (300.0, 1480.0)
#: (300.0, 1490.0)
#: (300.0, 1500.0)
del mdb.models['Model-1']
p = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
del mdb.models['Thermal'].materials['AA2319']
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
del mdb.models['Thermal'].materials['AA2319']
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
#: 
#: Point 1: 600.E-03, 600.E-03, 1.3  Point 2: 600.E-03, 600.E-03, 1.1
#:    Distance: 200.E-03  Components: 0., 0., -200.E-03
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#* ImportError: cannot import name Material
#* File "C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py", line 
#* 29, in <module>
#*     from material import Material
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#* ImportError: cannot import name Material
#* File "C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py", line 
#* 29, in <module>
#*     from material import Material
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#* ImportError: cannot import name Material
#* File "C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py", line 
#* 29, in <module>
#*     from material import Material
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#* ImportError: cannot import name Material
#* File "C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py", line 
#* 29, in <module>
#*     from material import Material
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
execfile('C:/Users/kariln/Documents/GitHub/Master/Abaqus/create_part.py', 
    __main__.__dict__)
#: The model "Thermal" has been created.
p1 = mdb.models['Thermal'].parts['Part_1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
