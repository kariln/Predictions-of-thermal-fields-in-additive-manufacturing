# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:50:07 2020

@author: kariln
"""

#add paths
import sys
from pathlib import Path

abaqus_path = Path('../')
sys.path.append(str(abaqus_path.resolve()))

from create_script import FEA_MODEL
from get_odb import Odb

"""THERMAL MODEL"""
scripted_part = FEA_MODEL('one-layer.py')
scripted_part.clear_variables()
scripted_part.imports(['part','material','section','assembly','step','interaction','load','mesh','job','sketch','visualization','connectorBehavior', 'customKernel','amModule', 'amKernelInit', 'amConstants', 'copy','os'])
scripted_part.include_paths([])
models = {}

#MODEL
thermal = scripted_part.create_model('thermal')
models.update({thermal.get_model_name():thermal})

#PART
part1 = scripted_part.create_part('part1', thermal, 'THREE_D','DEFORMABLE_BODY')
scripted_part.baseExtrude(part1, (-0.1,-0.1), (0.1,0.1), 0.02)
scripted_part.add_extrude(part1,(-0.06,-0.06),(0.06,0.06),0.0023,1)

#PROPERTY
scripted_part.assign_material('AA2319',[['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], thermal)
scripted_part.assign_section('AA2319',part1,'Part_Section')

#ASSEMBLY
scripted_part.create_instance(part1)

#STEP
scripted_part.create_heat_step('heat','Initial',4000,0.01,1E-8,1,1000, 10000,thermal)

#MESH
scripted_part.create_mesh(part1,0.01)

#LOAD
scripted_part.create_node_BC(part1)

#PREDEFINED FIELD
scripted_part.set_room_temp(part1, 20)

#FIELD OUTPUT
scripted_part.set_field_output(thermal, ['NT','TEMP'])

#AM MODEL
am_Model = scripted_part.create_thermal_AM_model(part1,'AM_thermal')
scripted_part.add_event_series(am_Model, 0.01,'zigzag',5000,100)
scripted_part.add_table_collections(am_Model,0.9)
scripted_part.add_simulation_setup(am_Model)

#JOB
scripted_part.create_job(thermal, 'one_layer_thermal')
#scripted_part.submit_job('experiment1_thermal')
