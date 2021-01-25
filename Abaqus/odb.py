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
        self.write('nodes = []\n')
        self.write('for element in add_elements[0]:\n')
        self.write('\ttemp = element.connectivity\n')
        self.write('\tfor i in temp:\n')
        self.write('\t\tif i not in nodes:\n')
        self.write('\t\t\tnodes.append(i)\n')
        self.write('assembly=odb.rootAssembly\n')
        self.write("assembly.NodeSetFromNodeLabels(name='NODE_ADD_SET', nodeLabels=(('PART1',nodes),))\n")
        self.seperate_sec()

    def get_temperature(self,base_depth):
        self.write('#GET TEMPERATURE\n')
        self.write('base_depth = ' + str(base_depth) + '\n')
        self.write("dispFile = open('disp.txt','w')\n")
        self.write("dispFile.write('i,t,T,x,y,z\\n')\n")
        self.get_frames()
        self.write("for frame in frames:\n")
        self.write("\ttime = frame.frameValue\n")
        self.write("\ttemperature = frame.fieldOutputs['NT11']\n")
        self.write("\tposition = frame.fieldOutputs['COORD']\n")
        self.write("\tfor i in range(0,len(temperature.values)):\n")
        self.write("\t\tpos = position.values[i]\n")
        self.write("\t\tif pos.data[2] > base_depth:\n")
        self.write("\t\t\ttemp = temperature.values[i]\n")
        self.write("\t\t\ti = temp.nodeLabel\n")
        self.write("\t\t\tt = time\n")
        self.write("\t\t\tT = temp.data\n")
        self.write("\t\t\tx = pos.data[0]\n")
        self.write("\t\t\ty = pos.data[1]\n")
        self.write("\t\t\tz = pos.data[2]\n")
        self.write("\t\t\tif T != 20.0:\n")
        self.write("\t\t\t\tdispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + '\\n')\n")
        self.write("dispFile.close()\n")
        
    def create_excel(self):
        workbook = xlsxwriter.Workbook('temperatures.xlsx')
        worksheet = workbook.add_worksheet()
        
    def write_excel(self, row, col, data, worksheet):
        worksheet.write(row, col, data)
        
    def end_excel(self, workbook):
        workbook.close()


dispFile = open('disp.txt','w')
dispFile.write('i,t,T,x,y,z')



