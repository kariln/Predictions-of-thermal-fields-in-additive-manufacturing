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
        baseExtrude = Feature(feature_name, part, point1, point2, depth)
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
        
    def add_extrude(self, feature_name,part, point1, point2, depth):
        add_extrude = Feature(feature_name, part, point1, point2, depth)
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

# #partition AM into layers
# nr_layers = 4
# plane_offset = 0.5
# for i in range(0,nr_layers):
#     datum_id = part1.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id
#     plane = part1.datums[datum_id]
#     plane_offset += 0.2
#     part1_cells = part1.cells
#     top_cell = part1_cells.findAt(((0.,0.,1.3),))
#     part1.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)
        
def main():
    scripted_part = AM_CAD('scripted_part.py')
    scripted_part.clear_variables()
    scripted_part.imports(['part','material','section','assembly','step','interaction','load','mesh','job','sketch','visualization','connectorBehavior', 'customKernel','amModule'])
    scripted_part.include_paths([r'C:\Users\kariln\Documents\GitHub\Master\Materials',r'C:\Users\Kari Ness\abaqus_plugins\AM plugin\AMModeler\AMModeler'])
    
    models = {}
    
    #creating model
    thermal = scripted_part.create_model('thermal')
    models.update({thermal.get_model_name():thermal})

    #creating part
    part1 = scripted_part.create_part('part1', thermal, 'THREE_D','DEFORMABLE_BODY')
    scripted_part.baseExtrude('base_extrude', part1, (-1.0,-1.0), (1.0,1.0), 0.5)
    scripted_part.add_extrude('add_element',part1,(-0.6,-0.6),(0.6,0.6),0.8)
main()
