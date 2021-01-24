import os
clear = lambda: os.system('cls')
clear()

#importing modules
import abaqus
from abaqus import *
import abaqusConstants
from abaqusConstants import *
import odbAccess
from odbAccess import *
import os
from os import *

odb = openOdb('experiment1_thermal.odb')

instance = odb.rootAssembly.instances['PART1']
add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']

add_elements = add_set.elements
session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_NODAL, variable=(('TEMP', INTEGRATION_POINT), ), elementSets=("ADD_ELEMENT", ))
