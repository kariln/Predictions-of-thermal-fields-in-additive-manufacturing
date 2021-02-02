# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 17:15:39 2021

@author: kariln
"""

#add paths
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
scripted_part = FEA_MODEL('experiment_4.py')
scripted_part.clear_variables()
scripted_part.imports(['part','material','section','assembly','step','interaction','load','mesh','job','sketch','visualization','connectorBehavior', 'customKernel','amModule', 'amKernelInit', 'amConstants', 'copy','os'])
scripted_part.include_paths([])
models = {}

#MODEL
thermal = scripted_part.create_model('thermal')
models.update({thermal.get_model_name():thermal})

#PART
part_name = 'part1'
part1 = scripted_part.create_part(part_name, thermal, 'THREE_D','DEFORMABLE_BODY')
base_depth = 0.02
scripted_part.baseExtrude(part1, (-0.05,-0.05), (0.05,0.05), base_depth)
point1 = (-0.04,-0.04)
point2 = (0.04,0.04)
scripted_part.add_extrude(part1,point1,point2,0.0092,3)

#PROPERTY
scripted_part.assign_material('AA2319',[['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], thermal)
scripted_part.assign_section('AA2319',part1,'Part_Section')

#ASSEMBLY
scripted_part.create_instance(part1)

#STEP
scripted_part.create_heat_step('heat','Initial',1000,0.01,1E-8,1,1000, 10000,thermal)

#MESH
scripted_part.create_mesh(part1,0.005)

#LOAD
scripted_part.create_node_BC(part1)

#PREDEFINED FIELD
scripted_part.set_room_temp(part1, 20)

#FIELD OUTPUT
scripted_part.set_field_output(thermal, ['NT','TEMP'])

#AM MODEL
am_Model = scripted_part.create_thermal_AM_model(part1,'AM_thermal')
Q = 5000
deposition_pattern = 'raster'
scripted_part.add_event_series(am_Model, 0.05,deposition_pattern,Q,10)
scripted_part.add_table_collections(am_Model,0.9)
scripted_part.add_simulation_setup(am_Model)

#JOB
scripted_part.create_job(thermal, 'experiment4_thermal')
scripted_part.submit_job('experiment4_thermal')

""" MECHANICICAL MODEL"""

""" ODB """
process_odb = Odb('experiment4_thermal',scripted_part, part1)
process_odb.clear_variables()
process_odb.imports(['abaqus','abaqusConstants','odbAccess'])
process_odb.open_odb()
process_odb.get_temperature(base_depth, part_name,point1, point2,deposition_pattern)