# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#
# Script to read data from odb file and save it to a csv file
#
import sys
import os
from create_script import FEA_MODEL
import xlsxwriter
from part import Part

class Odb:
    def __init__(self, job_name,CAD, part):
        self.job_name = job_name
        self.file_name = job_name + '_odb.py'
        self.file = open(self.file_name,"w+")
        self.file.truncate(0) 
        self.file.close()
        self.CAD = CAD
        self.work_dir = CAD.get_work_dir()
        
        
    def get_file_name(self):
        return self.file_name
    
    def get_job_name(self):
        return self.job_name
    
    def get_work_dir(self):
        return self.work_dir
    
    def get_full_path(self):
        path = self.get_work_dir()
        file_name = self.get_file_name()
        fullPath = os.path.join(path, file_name) 
        return fullPath
    
    def get_CAD(self):
        return self.CAD
    

        
    def write(self, string):
        file = open(self.get_file_name(), 'a')
        file.write(string)
        file.close()
        
    def imports(self,import_list):
        self.write('#importing modules\n')
        for elem in import_list:
            self.write('import ' + str(elem) + '\n')
            self.write('from ' + str(elem) + " import *\n")
        self.seperate_sec()
        
        
    def seperate_sec(self):
        #create sections in code
        self.write('\n')
        
    def clear_variables(self):
        #deleting all variables in Abaqus
        self.write("import os\n")
        self.write("clear = lambda: os.system('cls')\n")
        self.write("clear()\n")       
        self.seperate_sec()
        
    def open_odb(self):
        file_name = self.get_file_name()
        #create new folder for resulting files if it does not exist
        newFolder = "Resultat "+ file_name.split(".")[0]
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
        self.write("odb = openOdb('" + self.get_job_name() + ".odb')\n")
        self.seperate_sec()
        
    def get_add_elements(self, part_name):
        CAD = self.get_CAD()
        self.write("instance = odb.rootAssembly.instances['" + part_name.upper() + "']\n" )
        self.write("add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']\n")
        self.write("add_elements = add_set.elements[0]\n")
        self.seperate_sec()
        
    def get_step_name(self):
        self.write("stepName = odb.steps.keys()[0]\n")
        self.seperate_sec()
        
    def get_frames(self):
        self.get_step_name()
        self.write("frames = odb.steps[stepName].frames\n")
        
    def get_nr_frames(self):
        self.get_step_name(self)
        self.write("numberOfFrames = len(odb.steps['stepName'].frames)\n")
        
    def get_last_frame(self):
        self.get_step_name()
        self.write("lastFrame = odb.steps[stepName].frames[-1]\n")
        
    def get_add_nodes(self):
        self.write('\tnodes = []\n')
        self.write('\tfor element in add_elements:\n')
        self.write('\t\ttemp = element.connectivity\n')
        self.write('\t\tfor i in temp:\n')
        self.write('\t\t\tif i not in nodes:\n')
        self.write('\t\t\t\tnodes.append(i)\n')
        #self.write('assembly=odb.rootAssembly\n')
        #self.write("assembly.NodeSetFromNodeLabels(name='NODE_ADD_SET', nodeLabels=(('PART1',nodes),))\n")
        self.seperate_sec()

    def get_temperature(self,base_depth, part_name):
        self.get_add_elements(part_name)
        self.write('#GET TEMPERATURE\n')
        self.write('base_depth = ' + str(base_depth) + '\n')
        self.write("dispFile = open('disp.txt','w')\n")
        self.write("dispFile.write('i,t,T,x,y,z,Q_x,Q_y_,Q_z\\n')\n")
        self.get_frames()
        self.write("for frame in frames:\n")
        self.write("\ttime = frame.frameValue\n")
        self.write("\tif time > 2000:\n")
        self.write("\t\traise SystemExit(0)\n")
        self.get_active_elements()
        #self.get_add_nodes()
        self.write("\ttemperature = frame.fieldOutputs['NT11']\n")
        self.write("\tposition = frame.fieldOutputs['COORD']\n")
        self.get_laser_position()
        self.get_laser_position()
        self.write("\tfor i in range(0,len(temperature.values)):\n")
        self.write("\t\tpos = position.values[i]\n")
        self.write("\t\ttemp = temperature.values[i]\n")
        self.write("\t\tif temp.nodeLabel in active_nodes:\n")
        self.write("\t\t\ti = temp.nodeLabel\n")
        self.write("\t\t\tt = time\n")
        self.write("\t\t\tT = temp.data\n")
        self.write("\t\t\tx = pos.data[0]\n")
        self.write("\t\t\ty = pos.data[1]\n")
        self.write("\t\t\tz = pos.data[2]\n")
        self.write("\t\t\tdispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(Q_x) + ',' + str(Q_y) + ',' + str(Q_z) + '\\n')\n")
        self.write("dispFile.close()\n")
        
    def get_laser_position(self):
        self.write("#get laser position for frame\n")
        self.write("\tlast_nodes_labels = active_nodes[-4::]\n")
        self.write("\tlast_nodes_x = []\n")
        self.write("\tlast_nodes_y = []\n")
        self.write("\tlast_nodes_z = []\n")
        self.write("\tfor j in reversed(range(0,len(position.values))):\n")
        self.write("\t\tpos = position.values[j]\n")
        self.write("\t\tif pos.nodeLabel in last_nodes_labels:\n")
        self.write("\t\t\tx = pos.data[0]\n")
        self.write("\t\t\ty = pos.data[1]\n")
        self.write("\t\t\tz = pos.data[2]\n")
        self.write("\t\t\tlast_nodes_x.append(x)\n")
        self.write("\t\t\tlast_nodes_y.append(y)\n")
        self.write("\t\t\tlast_nodes_z.append(z)\n")
        self.write("\t\t\tif len(last_nodes_x) == 4:\n")
        self.write("\t\t\t\tbreak\n")
        self.write("\tif active_nodes != []:\n")
        self.write("\t\tQ_z = max(last_nodes_z)\n")
        self.write("\t\tQ_x = sum(last_nodes_x) / len(last_nodes_x)\n")
        self.write("\t\tQ_y = sum(last_nodes_y) / len(last_nodes_y)\n")
        
    def get_active_elements(self):
        self.write("#find active elements for frame\n")
        self.write("\tactive = frame.fieldOutputs['EACTIVE'].values\n")
        self.write("\tactive_elements = []\n")
        self.write("\tactive_nodes = []\n")
        self.write("\tfor i in range(0,len(active)):\n")
        self.write("\t\tif active[i].data == 1.0:\n")
        self.write("\t\t\tactive_elements.append(active[i].elementLabel)\n")
        self.write('\t\t\tfor element in add_elements:\n')
        self.write("\t\t\t\tif element.label in active_elements:\n")
        self.write('\t\t\t\t\ttemp = element.connectivity\n')
        self.write('\t\t\t\t\tfor i in temp:\n')
        self.write('\t\t\t\t\t\tif i not in active_nodes:\n')
        self.write('\t\t\t\t\t\t\tactive_nodes.append(i)\n')
        self.seperate_sec()

    def create_excel(self):
        workbook = xlsxwriter.Workbook('temperatures.xlsx')
        worksheet = workbook.add_worksheet()
        
    def write_excel(self, row, col, data, worksheet):
        worksheet.write(row, col, data)
        
    def end_excel(self, workbook):
        workbook.close()


#import os
#clear = lambda: os.system('cls')
#clear()
#
##importing modules
#import abaqus
#from abaqus import *
#import abaqusConstants
#from abaqusConstants import *
#import odbAccess
#from odbAccess import *
#from statistics import mean 
#
#odb = openOdb('experiment1_thermal.odb')
#
#instance = odb.rootAssembly.instances['PART1']
#add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
#add_elements = add_set.elements[0]
#
#stepName = odb.steps.keys()[0]
#
#frames = odb.steps[stepName].frames
#instance = odb.rootAssembly.instances['PART1']
#add_set = odb.rootAssembly.elementSets['ADD_ELEMENT']
#add_elements = add_set.elements[0]
#
##GET TEMPERATURE
#base_depth = 0.02
#dispFile = open('disp.txt','w')
#dispFile.write('i,t,T,x,y,z\n')
#stepName = odb.steps.keys()[0]
#
#frames = odb.steps[stepName].frames
#for frame in frames:
#	time = frame.frameValue
#	if time > 2000:
#		raise SystemExit(0)
##find active elements for frame
#	active = frame.fieldOutputs['EACTIVE'].values
#	active_elements = []
#	active_nodes = []
#	for i in range(0,len(active)):
#		if active[i].data == 1.0:
#			active_elements.append(active[i].elementLabel)
#			for element in add_elements:
#				if element.label in active_elements:
#					temp = element.connectivity
#					for i in temp:
#						if i not in active_nodes:
#							active_nodes.append(i)
#
#	temperature = frame.fieldOutputs['NT11']
#	position = frame.fieldOutputs['COORD']
#    #find laser position
#    last_nodes_labels = active_nodes[-4::]\n")
#    last_nodes_x = []
#    last_nodes_y = []
#    last_nodes_z = []
#    for j in reversed(range(0,len(position.values))):
#        pos = position.values[j]
#        if pos.nodeLabel in last_nodes_labels:
#            x = pos.data[0]
#			y = pos.data[1]
#			z = pos.data[2]
#            last_nodes_x.append(x)
#            last_nodes_y.append(y)
#            last_nodes_z.append(z)
#            if len(las_nodes_x) == 4:
#                break:
#    Q_z = max(last_nodes_z)
#    Q_x = sum(last_nodes_x) / len(last_nodes_x) 
#    Q_y = sum(last_nodes_y) / len(last_nodes_y) 
#	for i in range(0,len(temperature.values)):
#		pos = position.values[i]
#		temp = temperature.values[i]
#		if temp.nodeLabel in active_nodes:
#			i = temp.nodeLabel
#			t = time
#			T = temp.data
#			x = pos.data[0]
#			y = pos.data[1]
#			z = pos.data[2]
#			dispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + '\n')
#dispFile.close()



