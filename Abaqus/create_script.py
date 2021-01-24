# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:14:46 2020

@author: kariln

Class created for automatic creation of AM CAD models. 
Assumptions:
    Features are rectangular
    Midpoint of sketch is 0,0
    Sketch plane is XY
"""
#add paths
import sys
import os
from pathlib import Path

material_path = Path('../Materials')
sys.path.append(str(material_path.resolve()))

deposition_path = Path('../Deposition_Patterns')
sys.path.append(str(deposition_path.resolve()))

#importing classes
from model import Model
from part import Part
from feature import Feature
from material import Material
from mesh import Mesh
from sets import Set
from zigzag import Zigzag
from raster import Raster
from job import Job
import pathlib
from amModel import AM


class FEA_MODEL:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name,"w+")
        self.file.truncate(0) 
        self.file.close()
        self.work_dir=None
        self.jobs = {}

    def get_file_name(self):
        return self.file_name
        
    def write(self, string):
        file = open(self.get_file_name(), 'a')
        file.write(string)
        file.close()
        
    def seperate_sec(self):
        #create sections in code
        self.write('\n')
        
    def clear_variables(self):
        #deleting all variables in Abaqus
        self.write("import os\n")
        self.write("clear = lambda: os.system('cls')\n")
        self.write("clear()\n")       
        self.seperate_sec()
        
    def imports(self,import_list):
        self.write('#importing modules\n')
        for elem in import_list:
            self.write('import ' + str(elem) + '\n')
            self.write('from ' + str(elem) + " import *\n")
        self.write('session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)\n')
        self.seperate_sec()
        
    def include_paths(self,path_list):
        self.write('#Include paths\n')
        self.write('import sys\n')
        user_path = Path('../../../..')

        for elem in path_list:
            self.write("sys.path.append(r'" + elem +"')\n")
            
        plugin_path = Path(user_path / 'abagus_plugins' / 'AM plugin' / 'AMModeler' / 'AMModeler')
        self.write("sys.path.append(r'" + str(plugin_path.resolve()) + "')\n" )
        self.seperate_sec()
            
    def create_model(self,model_name):
        self.write('#MODEL\n')
        model = Model(model_name)
        self.write(model.get_model_name() +" = mdb.Model(name= '" + model.get_model_name() + "')\n")
        self.write("mdb.models['" + model_name + "'].setValues(absoluteZero=-273.15, stefanBoltzmann=5.67E-08)\n")
        self.seperate_sec()
        return model
        
    def create_part(self,part_name, model, dimensionality,part_type):
        self.write('#PART\n')
        part = Part(part_name, model,dimensionality,part_type)
        part_name = part.get_part_name()
        dimensionality = part.get_dimensionality()
        part_type = part.get_part_type()
        model_name = model.get_model_name()
        self.write(part_name + "=" + model_name + ".Part(dimensionality =" + dimensionality + " , name= '"+ part_name + "' , type = " + part_type + ")\n")
        self.write('f, e = ' + part_name + '.faces, ' + part_name + '.edges #getting the edges and faces of the part\n')
        model.add_part(part)
        self.seperate_sec()
        return part
        
    def baseExtrude(self, part, point1, point2, depth):
        baseExtrude = Feature(part, point1, point2, depth, 1)
        baseExtrude.set_feature_name('base_element')
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        self.write('#extrusion of base\n')
        sheetSize = abs(2*(point1[0]-point2[0])*(point1[1]-point2[1]))
        self.write('sketch_name = ' + model_name + ".ConstrainedSketch(name='__profile__',sheetSize= " + str(sheetSize) + ')\n')
        point1_str = str(point1)
        point2_str = str(point2)
        self.write('sketch_name.rectangle(point1=' + point1_str + ',point2=(' + point2_str + '))\n')
        self.write(part_name + '.BaseSolidExtrude(sketch=sketch_name,depth=' + str(depth) + ')\n')
        self.write('e = ' + part_name + '.edges\n')
        self.write('del ' + model_name + ".sketches['__profile__']\n")
        part.add_feature(baseExtrude)
        self.seperate_sec()
        
    def add_extrude(self,part, point1, point2, depth, nr_layers):
        add_extrude = Feature(part, point1, point2, depth, nr_layers)
        add_extrude.set_feature_name('add_element')
        base = part.get_features()['base_element']
        sheetSize = abs(2*(base.get_point1()[0]-base.get_point2()[0])*(base.get_point1()[1]-base.get_point2()[1]))
        sketch_plane = (0.,0.,base.get_depth())
        self.write('substrate_top_plane = f.findAt((' + str(sketch_plane) + ',))[0]\n')
        up_edge = (0.,base.get_point2()[1], base.get_depth())
        part_name = part.get_part_name()
        model_name = part.get_model_name()
        self.write('sketch_UpEdge = e.findAt((' + str(up_edge) + ',))[0]\n')
        self.write('sketch_transform = ' + part_name + '.MakeSketchTransform(sketchPlane = substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,origin=(0.0,0.0,' + str(base.get_depth()) + '))\n')
        self.write('AM_sketch = ' + part.get_model_name() + ".ConstrainedSketch(name = '__profile__',sheetSize=" + str(sheetSize) + ',gridSpacing=0.14, transform=sketch_transform)\n')
        self.write('AM_sketch.rectangle(point1=' + str(point1) + ',point2=' + str(point2) + ')\n')
        self.write(part_name + '.SolidExtrude(depth=' + str(depth) + ',sketchPlane=substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,sketch = AM_sketch,flipExtrudeDirection=OFF)\n')
        self.write('del ' + model_name + ".sketches['__profile__']\n")
        self.write('#partition AM into layers')
        self.write('\nnr_layers = ' + str(nr_layers) + '\n')
        plane_offset = base.get_depth()
        layer_thickness = depth/nr_layers
        self.write('plane_offset = ' + str(plane_offset) + '\n')
        self.write('for i in range(0,nr_layers):\n')
        self.write('\tdatum_id = '+ part_name + '.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id\n')
        self.write('\tplane = ' + part_name + '.datums[datum_id]\n')
        self.write('\tplane_offset += ' + str(layer_thickness) + '\n')
        self.write('\t' + part_name + '_cells = ' + part_name + '.cells\n')
        self.write('\ttop_cell = ' + part_name + '_cells.findAt(((0.,0.,' + str(base.get_depth() + depth) + '),))\n')
        self.write('\t' + part_name + '.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)\n')
        part.add_feature(add_extrude)
        self.seperate_sec()
        
    def assign_material(self, material_name, material_properties, model):
        self.write('#PROPERTY\n')
        material = Material(material_properties, material_name)
        material_name = material.get_material_name()
        model_name = model.get_model_name()
        self.write(material_name + ' = ' + model_name + ".Material(name='" + material_name + "')\n")
        for prop in material_properties:
            property_name = prop[0]
            temperatureDependency = prop[1]
            property_table = material.get_property_table(property_name)
            if temperatureDependency is not None:
                self.write(material_name + '.' + property_name + '(temperatureDependency=' + temperatureDependency + ',table=' + str(property_table) + ')\n')
            else:
                self.write(material_name + '.' + property_name + '(table=' + str(property_table) + ')\n')
        model.add_material(material)
        self.seperate_sec()
        
    def assign_section(self, material_name, part, section_name):
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        self.write(model_name + ".HomogeneousSolidSection(name='" + section_name + "', material='" + material_name + "', thickness=None)\n")
        self.write('c = ' + part_name + '.cells\n')
        self.write('region = ' + part_name + '.Set(cells = c, name = "full_part")\n')
        full_part = Set(part,'full_part')
        part.add_set(full_part)
        self.write(part_name + ".SectionAssignment(region=region, sectionName='" + section_name + "', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)\n")
        self.seperate_sec()
        
    def create_instance(self, part):
        self.write('#ASSEMBLY\n')
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        self.write('a = ' + model_name + '.rootAssembly\n')
        self.write('a.DatumCsysByDefault(CARTESIAN)\n')
        self.write("a.Instance(name='" + part_name + "', part= " + part_name + ", dependent=ON)\n")
        self.seperate_sec()
        
    def create_heat_step(self, step_name, previous, timePeriod, initialInc, minInc,maxInc,deltmx, maxNumInc, model):
        self.write('#STEP\n')
        model_name = model.get_model_name()
        self.write(model_name + ".HeatTransferStep(name='" + step_name + "', previous='" + previous +"', timePeriod=" + str(timePeriod) + ', initialInc=' + str(initialInc) + ', minInc=' + str(minInc) + ', maxInc=' + str(maxInc) + ',deltmx=' + str(deltmx) + ',maxNumInc=' + str(maxNumInc) +')\n')
        self.seperate_sec()
        
    def create_mesh(self, part, road_width):
        self.write('#MESH\n')
        part_name = part.get_part_name()
        #makes global seed half of the road width
        globalSeed = road_width/2
        #creating mesh object
        mesh = Mesh(part,globalSeed)
        part.create_mesh(mesh)
        self.write(part_name + '.seedPart(size=' + str(globalSeed) + ', deviationFactor=0.1, minSizeFactor=0.1)\n')
        #self.write(part_name + '.seedEdgeBySize(edges=substrate_edges, size=' + str(localSeed) + ', deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)\n')
        self.write('e = ' + part_name + '.edges\n')
        self.write(part_name + '.generateMesh()\n')
        self.write('elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD)\n') #heat transfer element type
        self.write('elemType2 = mesh.ElemType(elemCode=DC3D6, elemLibrary=STANDARD)\n')
        self.write('elemType3 = mesh.ElemType(elemCode=DC3D4, elemLibrary=STANDARD)\n')
        self.write('c = ' + part_name + '.cells\n')
        self.write('region = ' + part_name + '.Set(cells = c, name = "part")\n')
        part_set = Set(part, 'part')
        part.add_set(part_set)
        self.write(part_name + '.setElementType(regions=region, elemTypes=(elemType1,elemType2,elemType3))\n')
        self.seperate_sec()
        
    def create_node_BC(self, part):
        self.write('#BOUNDARY CONDITION\n')
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        mesh = part.get_mesh()
        globalSeed = mesh.get_global_seed()
        radius = globalSeed/2 #radius of boundingsphere which is half of the globalSeed to ensure only getting the origo node
        self.write('n = '+ part_name + '.nodes\n')
        self.write('origo_node = n.getByBoundingSphere(center = (0.,0.,0.), radius = ' + str(radius) +')\n')
        self.write(part_name + '.Set(nodes=origo_node, name="origo_node")\n')
        self.write('a = ' + model_name + '.rootAssembly\n')
        self.write('region = a.instances["' + part_name + '"].sets["origo_node"]\n')
        self.write(model_name + '.DisplacementBC(name="origo_BC", createStepName="Initial", region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName="", localCsys=None)\n')
        self.seperate_sec()
        
    def set_room_temp(self,part, roomtemp):
        self.write('#PREDEFINED FIELDS\n')
        part_name = part.get_part_name()
        model_name = part.get_model_name()
        self.write('nodes1 = ' + part_name + '.nodes\n')
        self.write(part_name + '.Set(nodes=nodes1, name="all_nodes")\n')
        all_nodes = Set(part, 'all_nodes')
        part.add_set(all_nodes)
        self.write('a = ' + model_name + '.rootAssembly\n')
        self.write('region = a.instances["' + part_name + '"].sets["all_nodes"]\n')
        self.write(model_name + '.Temperature(name="room_temp", createStepName="Initial", region=region, distributionType=UNIFORM, crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(' + str(roomtemp) + ', ))\n')
        self.seperate_sec()
        
    def set_field_output(self, model, variables):
        model_name = model.get_model_name()
        self.write(model_name + ".fieldOutputRequests['F-Output-1'].setValues(variables=(")
        for variable in variables:
            self.write("'" + variable + "'")
            if variable != variables[-1]:
                self.write(',')
        self.write('))\n')
        self.seperate_sec()

    def create_thermal_AM_model(self,part,amModel_name):
        self.write('#AM PART\n')
        am_Model = AM(part,amModel_name)
        part.add_amModel(am_Model)
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        self.write("amModule.createAMModel(amModelName='" + amModel_name + "', modelName1='" + model_name +"', stepName1='heat', analysisType1=HEAT_TRANSFER, isSequential=OFF, modelName2='', stepName2='', analysisType2=STRUCTURAL, processType=AMPROC_ABAQUS_BUILTIN)\n")
        self.write('a = ' + model_name + '.rootAssembly\n')
        self.write('a.regenerate()\n')
        AM_model_name = 'mdb.customData.am.amModels["' + amModel_name + '"]'
        self.write(AM_model_name + '.assignAMPart(amPartsData=(("' + part_name + '", "Build Part"), ("", ""), ("", ""), ("", ""), ("", "")))\n')
        self.seperate_sec()
        return am_Model
        
    def add_event_series(self,am_Model, road_width, deposition_pattern, power, layer_break):
        self.write('#EVENT SERIES\n')
        part = am_Model.get_part()
        amModel_name = am_Model.get_amModel_name()
        AM_model_name = 'mdb.customData.am.amModels["' + amModel_name + '"]'
        
        add_element = part.get_features()['add_element']
        base_element = part.get_features()['base_element']
        
        #depth of add_element
        depth = add_element.get_depth()
        
        #thickness of each layer
        thickness = add_element.get_layer_thickness()
        
        #road_width
        am_Model.set_road_width(road_width)
        
        #corner coordinate
        point1 = add_element.get_point1()
        corner_x = point1[0]
        corner_y = point1[1]
        corner_z = base_element.get_depth()
        
        #x and y length of add_element
        point2 = add_element.get_point2()
        x_length = abs(point1[0]-point2[0])
        y_length = abs(point1[1]-point2[1])

        if deposition_pattern.lower() == 'raster':
            #__init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
            dp_object = Raster(depth, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,power, layer_break)
        elif deposition_pattern.lower() == 'zigzag':
            #__init__(self, z_length, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,P):
            dp_object = Zigzag(depth, thickness, x_length, y_length, corner_x, corner_y, corner_z, road_width,power, layer_break)
        else: 
            raise NotImplementedError('This deposition pattern is not implemented');
            
        dp_object.generate_heat_path()
        dp_object.generate_material_path()
        material_path = pathlib.Path('material_path.txt')
        material_path = material_path.resolve()
        heat_path = pathlib.Path('heat_path.txt')
        heat_path = heat_path.resolve()
        print(heat_path)
        print(material_path)
        self.write(AM_model_name + '.addEventSeries(eventSeriesName="material_path", eventSeriesTypeName=' + "'" + '"ABQ_AM.MaterialDeposition"' + "'" + ', timeSpan="TOTAL TIME", fileName="'+ str(material_path) +'", isFile=ON)\n')
        self.write(AM_model_name + '.addEventSeries(eventSeriesName="heat_path", eventSeriesTypeName=' + "'" + '"ABQ_AM.PowerMagnitude"' + "'" + ', timeSpan="TOTAL TIME", fileName="' + str(heat_path) + '", isFile=ON)\n')        
        self.seperate_sec()
        
    def add_table_collections(self,am_Model, absorption_coefficient):
        self.write('#TABLE COLLECTIONS\n')
        part = am_Model.get_part()
        amModel_name = am_Model.get_amModel_name()
        AM_model_name = 'mdb.customData.am.amModels["' + amModel_name + '"]'
        add_element = part.get_features()['add_element']
        
        #thickness of each layer in add_element
        thickness = add_element.get_layer_thickness()
        
        #road_width of each layer
        road_width = am_Model.get_road_width()
        if road_width == None:
            raise Exception("Must create event series before table collections")
            
        #activation offset - how much each bead is offseted
        activation_offset = road_width/2
        am_Model.set_activation_offset(activation_offset)
        
        #absorption coefficient
        am_Model.set_absorption_coefficient(absorption_coefficient)
        
        self.write(AM_model_name + '.addTableCollection(tableCollectionName="ABQ_AM_Material")\n')
        self.write(AM_model_name + '.dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name=' + "'_parameterTable_" + '"ABQ_AM.MaterialDeposition.Advanced"_' + "', parameterTabletype='" + '"ABQ_AM.MaterialDeposition.Advanced"' + "', parameterData=(('Full', 0.0, 0.0), ))\n")
        self.write(AM_model_name + '.dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name = ' + "'_parameterTable_" + '"ABQ_AM.MaterialDeposition.Bead"_' + "', parameterTabletype='" + '"ABQ_AM.MaterialDeposition.Bead"' + "', parameterData=(('Z', " + str(thickness) + "," + str(road_width) +"," + str(activation_offset) + ", 'Below'), ))\n")
        self.write(AM_model_name + '.dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name = ' + "'_parameterTable_" + '"ABQ_AM.MaterialDeposition"_' + "', parameterTabletype='" + '"ABQ_AM.MaterialDeposition"' + "', parameterData=(('material_path', 'Bead'), ))\n")
        
        self.write(AM_model_name + '.addTableCollection(tableCollectionName="ABQ_AM_Heat")\n')
        self.write(AM_model_name + ".dataSetup.tableCollections['ABQ_AM_Heat'].PropertyTable(name='_propertyTable_" + '"ABQ_AM.AbsorptionCoeff"_' + "', propertyTableType='" + '"ABQ_AM.AbsorptionCoeff"' + "', propertyTableData=((" + str(absorption_coefficient) +", ), ), numDependencies=0, temperatureDependency=OFF)\n")
        self.write(AM_model_name + ".dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_" + '"ABQ_AM.MovingHeatSource"_' + "', parameterTabletype='" + '"ABQ_AM.MovingHeatSource"' + "', parameterData=(('heat_path', 'Goldak'), ))\n")
        self.write(AM_model_name + ".dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_" + '"ABQ_AM.MovingHeatSource.Goldak"_' + "', parameterTabletype='" + '"ABQ_AM.MovingHeatSource.Goldak"' + "', parameterData=(('9', '9', '9', " + str(activation_offset) + ',' + str(thickness) + ', 0.002, 0.004, 0.6, 1.4, 1), ))\n')
        self.write(AM_model_name + ".dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_" + '"ABQ_AM.MovingHeatSource.Advanced"_' + "', parameterTabletype='" + '"ABQ_AM.MovingHeatSource.Advanced"' + "', parameterData=(('False', 'False', 'Relative', 0.0, 0.0, -1.0, 1.0), ))\n")
        self.seperate_sec()
        
    def add_simulation_setup(self, amModel):
        self.write("#SIMULATION SETUP\n")
        part = amModel.get_part()
        mesh = part.get_mesh()
        global_seed = mesh.get_global_seed()
        add_element = part.get_features()['add_element']
        base_element = part.get_features()['base_element']
        base_depth = base_element.get_depth()
        add_depth = add_element.get_depth()
        thickness = add_element.get_layer_thickness()
        total_depth = base_depth + add_depth
        point1 = add_element.get_point1()
        point2 = add_element.get_point2()
        part_name = part.get_part_name()
        model_name = part.get_model_name()
        amModel_name = amModel.get_amModel_name()
        AM_model_name = 'mdb.customData.am.amModels["' + amModel_name + '"]'
        self.write('a = ' + model_name + '.rootAssembly\n')
        self.write("e = a.instances['" + part_name + "'].elements\n")
        self.write('add_elements = e.getByBoundingBox(' + str(point1[0]) + ',' + str(point1[1]) + ',' + str(base_depth - global_seed/2) + ',' + str(point2[0]) + ',' + str(point2[1]) + ',' + str(total_depth + global_seed/2) + ')\n')
        self.write('a.Set(elements=add_elements, name="add_element")\n')
        self.write('f = a.instances["' + part_name + '"].faces\n')
        self.write('basement_face = f.findAt(((0.0,0.0,0.0) ,))\n')
        self.write('a.Set(faces=basement_face, name = "basement")\n')
        self.write('c = a.instances["' + part_name + '"].cells\n')
        #film contains basement -edit
        self.write('film = c.findAt(((' + str(point1[0]) + ',' + str(point1[1]/3) + ',' + str(base_depth + thickness/2) + '), ), ((' + str(point1[0]) + ',' + str(point1[1]/3) + ',' + str(base_depth + 3*thickness/2) + '), ),((' + str(point1[0]) + ',' + str(point1[1]/3) + ',' + str(base_depth + 5*thickness/2) + '),  ), ((' + str(point1[0]) + ',' + str(point1[1]/3) + ',' + str(base_depth) + '),  ))\n')
        self.write('a.Set(cells = film, name = "film")\n')
        #Material arrival:
        self.write(AM_model_name + ".addMaterialArrival(materialArrivalName='Material Source -1', tableCollection='ABQ_AM_Material', followDeformation=OFF, useElementSet=ON, elementSetRegion=('add_element', ))\n")
        
        #Heat source
        self.write(AM_model_name + ".addHeatSourceDefinition(heatSourceName='Heat Source -1', dfluxDistribution='Moving-UserDefined', dfluxMagnitude=1, tableCollection='ABQ_AM_Heat', useElementSet=OFF, elementSetRegion=())\n")
        
        #Cooling
        self.write(AM_model_name + ".addCoolingInteractions(coolingInteractionName='Film', useElementSet=ON, elementSetRegion=('film', ), isConvectionActive=ON, isRadiationActive=OFF, filmDefinition='Embedded Coefficient', filmCoefficient=8.5, filmcoefficeintamplitude='Instantaneous', sinkDefinition='Uniform', sinkTemperature=20, sinkAmplitude='Instantaneous', radiationType='toAmbient', emissivityDistribution='Uniform', emissivity=0.8, ambientTemperature=20, ambientTemperatureAmplitude='Instanteneous')\n")
        self.write(AM_model_name + ".addCoolingInteractions(coolingInteractionName='Basement', useElementSet=ON, elementSetRegion=('basement', ), isConvectionActive=ON, isRadiationActive=ON, filmDefinition='Embedded Coefficient', filmCoefficient=167, filmcoefficeintamplitude='Instantaneous', sinkDefinition='Uniform', sinkTemperature=20, sinkAmplitude='Instantaneous', radiationType='toAmbient', emissivityDistribution='Uniform', emissivity=0.8, ambientTemperature=20, ambientTemperatureAmplitude='Instanteneous')\n")
        
    def get_jobs(self):
        return self.jobs
        
    def add_job(self,job):
        job_name = job.get_job_name()
        self.get_jobs().update({job_name:job})
        
    def create_job(self, model, job_name):
        model_name = model.get_model_name()
        job = Job(job_name,model_name)
        self.add:job(job)
        self.write("mdb.Job(name='" + job_name + "', model='" + model_name + "', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=2, numDomains=2, numGPUs=0)\n")

    def submit_job(self,job_name):
        self.write("mdb.jobs['" + job_name + "'].submit(consistencyChecking=OFF)\n")
        
    def set_work_dir(self, path):
        self.work_dir = path
        path.replace('/','//')
        self.write('os.chdir(' + path + ')\n')
        
    def get_work_dir(self):
        return self.work_dir
        
    def save(self):
        path = self.get_work_dir()
        self.write("mdb.saveAs(pathName='" + path + "')\n")

    def create_mechanical(self, model_name, thermal_model_name):
        self.write("mdb.Model(name='" + model_name + "', objectToCopy=mdb.models['" + thermal_model_name + "'])\n")
        #kopiere modell
        #endre predefined fields: putt inn frames og odb
        #endre BC: substrate
        #endre steps
        #lag ny amModell med thermo-structural
        #endre element type
        #endre field output