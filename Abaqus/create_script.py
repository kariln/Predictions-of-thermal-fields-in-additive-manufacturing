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
#importing classes
from model import Model
from part import Part
from feature import Feature
from material import Material


class AM_CAD:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name,"w+")
        self.file.truncate(0) 
        self.file.close()
        
    def get_file(self):
        return self.file
    
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
        self.write('#importing modules')
        for elem in import_list:
            self.write('from ' + str(elem) + " import *\n")
        self.write('session.journalOptions.setValues(recoverGeometry=COORDINATE)\n')
        self.seperate_sec()
        
    def include_paths(self,path_list):
        self.write('#Include paths\n')
        self.write('import sys\n')
        for elem in path_list:
            self.write("sys.path.append(r'" + elem +"')\n")
        self.seperate_sec()
            
    def create_model(self,model_name):
        self.write('#MODEL\n')
        model = Model(model_name)
        self.write(model.get_model_name() +" = mdb.Model(name= '" + model.get_model_name() + "')\n")
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
        
    def baseExtrude(self, feature_name, part, point1, point2, depth):
        baseExtrude = Feature(feature_name, part, point1, point2, depth, 1)
        model_name = part.get_model_name()
        part_name = part.get_part_name()
        self.write('#extrusion of base\n')
        sheetSize = abs(2*(point1[0]-point2[0])*(point1[1]-point2[1]))
        self.write('sketch_name = ' + model_name + ".ConstrainedSketch(name='__profile__',sheetSize= " + str(sheetSize) + ')\n')
        point1_str = str(point1)
        point2_str = str(point2)
        self.write('sketch_name.rectangle(point1=' + point1_str + ',point2=(' + point2_str + '))\n')
        self.write(part_name + '.BaseSolidExtrude(sketch=sketch_name,depth=' + str(depth) + ')\n')
        self.write('del ' + model_name + ".sketches['__profile__']\n")
        part.add_feature(baseExtrude)
        self.seperate_sec()
        
    def add_extrude(self, feature_name,part, point1, point2, depth, nr_layers):
        add_extrude = Feature(feature_name, part, point1, point2, depth, nr_layers)
        base = part.get_features()['base_extrude']
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
        
    def create_heat_step(self, step_name, previous, timePeriod, initialInc, minInc,maxInc,deltmx, model):
        self.write('#STEP\n')
        model_name = model.get_model_name()
        self.write(model_name + ".HeatTransferStep(name='" + step_name + "', previous='" + previous +"', timePeriod=" + str(timePeriod) + ', initialInc=' + str(initialInc) + ', minInc=' + str(minInc) + ', maxInc=' + str(maxInc) + ',deltmx=' + str(deltmx) + ')\n')
        self.seperate_sec()

        
def main():
    scripted_part = AM_CAD('scripted_part.py')
    scripted_part.clear_variables()
    scripted_part.imports(['part','material','section','assembly','step','interaction','load','mesh','job','sketch','visualization','connectorBehavior', 'customKernel','amModule'])
    scripted_part.include_paths([r'C:\Users\kariln\Documents\GitHub\Master\Materials',r'C:\Users\Kari Ness\abaqus_plugins\AM plugin\AMModeler\AMModeler'])
    
    models = {}
    
    #MODEL
    thermal = scripted_part.create_model('thermal')
    models.update({thermal.get_model_name():thermal})

    #PART
    part1 = scripted_part.create_part('part1', thermal, 'THREE_D','DEFORMABLE_BODY')
    scripted_part.baseExtrude('base_extrude', part1, (-1.0,-1.0), (1.0,1.0), 0.5)
    scripted_part.add_extrude('add_element',part1,(-0.6,-0.6),(0.6,0.6),0.8,4)
    
    #PROPERTY
    scripted_part.assign_material('AA2319',[['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], thermal)
    scripted_part.assign_section('AA2319',part1,'Part_Section')
    
    #ASSEMBLY
    scripted_part.create_instance(part1)
    
    #STEP
    scripted_part.create_heat_step('heat','Initial',4000,0.01,1E-8,0.1,600, thermal)
    
main()
