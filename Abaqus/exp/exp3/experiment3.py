# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:48:23 2020

@author: kariln
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:22:28 2020

@author: kariln

Thermal experiment with zigzag pattern and cooling time 10s. between each layer
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


"""THERMAL MODEL"""
scripted_part = FEA_MODEL('experiment_3.py')
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
scripted_part.baseExtrude(part1, (-0.1,-0.1), (0.1,0.1), base_depth)
point1 = (-0.06,-0.06)
point2 = (0.06,0.06)
scripted_part.add_extrude(part1,point1,point2,0.0092,4)

#PROPERTY
scripted_part.assign_material('AA2319',[['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], thermal)
scripted_part.assign_section('AA2319',part1,'Part_Section')

#ASSEMBLY
scripted_part.create_instance(part1)

#STEP
scripted_part.create_heat_step('heat','Initial',4000,0.01,1E-8,1,1000, 10000,thermal)

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
scripted_part.add_event_series(am_Model, 0.01,'zigzag',Q,10)
scripted_part.add_table_collections(am_Model,0.9)
scripted_part.add_simulation_setup(am_Model)

#JOB
scripted_part.create_job(thermal, 'experiment1_thermal')
#scripted_part.submit_job('experiment1_thermal')

""" MECHANICICAL MODEL"""

""" ODB """
process_odb = Odb('experiment1_thermal',scripted_part, part1)
process_odb.clear_variables()
process_odb.imports(['abaqus','abaqusConstants','odbAccess'])
process_odb.open_odb()
process_odb.get_temperature(base_depth, part_name,Q, point1, point2)

