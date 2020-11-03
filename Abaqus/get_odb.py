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
    
    def get_work_dir(self):
        return self.work_dir
    
    def get_full_path(self):
        path = self.get_work_dir()
        file_name = self.get_file_name()
        fullPath = os.path.join(path, file_name) 
        return fullPath
        
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
        self.write("odb = openOdb('" + file_name + "')\n")


