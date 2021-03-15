# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:23:00 2021

@author: kariln
"""


import sys
from pathlib import Path

abaqus_path = Path('../../')
sys.path.append(str(abaqus_path.resolve()))

material_path = Path('../Materials')
sys.path.append(str(material_path.resolve()))

deposition_path = Path('../Deposition_Patterns')
sys.path.append(str(deposition_path.resolve()))

from create_script import FEA_MODEL
from odb import Odb


"""THERMAL MODEL"""
scripted_part = FEA_MODEL('experiment_7.py')
scripted_part.clear_variables()
scripted_part.imports(['part','material','section','assembly','step','interaction','load','mesh','job','sketch','visualization','connectorBehavior', 'customKernel','amModule', 'amKernelInit', 'amConstants', 'copy'])
scripted_part.include_paths([])
models = {}

#MODEL
thermal = scripted_part.create_model('thermal')
models.update({thermal.get_model_name():thermal})

#PART
part_name = 'part1'
part1 = scripted_part.create_part(part_name, thermal, 'THREE_D','DEFORMABLE_BODY')
base_depth = 0.02
base_point1 = (-0.05,-0.05)
base_point2 = (0.05,0.05)
scripted_part.baseExtrude(part1,base_point1 ,base_point2, base_depth)
point1 = (-0.04,-0.04)
point2 = (0.04,0.04)
add_depth = 0.003
nr_layer = 1
scripted_part.add_extrude(part1,point1,point2,add_depth,nr_layer)

#PROPERTY
scripted_part.assign_material('AA2319',[['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], thermal)
scripted_part.assign_section('AA2319',part1,'Part_Section')

#ASSEMBLY
scripted_part.create_instance(part1)

#STEP
timePeriod = 1000
initialInc = 0.01
minInc = 1E-8
maxInc = 1
deltmx = 1000
maxNumInc = 10000
scripted_part.create_heat_step('heat','Initial',timePeriod,initialInc,minInc,maxInc,deltmx, maxNumInc,thermal)

#MESH
road_width = 0.005
scripted_part.create_mesh(part1,road_width)

#LOAD
scripted_part.create_node_BC(part1)

#PREDEFINED FIELD
room_temp = 20
scripted_part.set_room_temp(part1, room_temp)

#FIELD OUTPUT
scripted_part.set_field_output(thermal, ['NT','TEMP','COORD','EACTIVE'])

#AM MODEL
am_Model = scripted_part.create_thermal_AM_model(part1,'AM_thermal')
Q = 4000
deposition_pattern = 'raster'
layer_break = 10
absorption_coefficient = 0.9
scripted_part.add_event_series(am_Model, road_width,deposition_pattern,Q,layer_break)
scripted_part.add_table_collections(am_Model,absorption_coefficient)
scripted_part.add_simulation_setup(am_Model)

#JOB
scripted_part.create_job(thermal, 'experiment7_thermal')
scripted_part.submit_job('experiment7_thermal')

""" MECHANICICAL MODEL"""

""" ODB """
process_odb = Odb('experiment7_thermal',scripted_part, part1)
process_odb.clear_variables()
process_odb.imports(['abaqus','abaqusConstants','odbAccess'])
process_odb.open_odb()
process_odb.get_temperature(base_depth, part_name,point1, point2,deposition_pattern,road_width)