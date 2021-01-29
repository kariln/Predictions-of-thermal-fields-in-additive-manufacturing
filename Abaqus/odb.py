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
        
    def get_free_surface_distance(self):
        self.write("\t\t\t\t\td_top = abs(Q_z-z)\n")
        self.write("\t\t\t\t\td_bottom = abs(z-base_depth)\n")
        self.write("\t\t\t\t\td_x1 = abs(point1[0]-x)\n")
        self.write("\t\t\t\t\td_x2 = abs(point2[0]-x)\n")
        self.write("\t\t\t\t\td_y1 = abs(point1[1]-y)\n")
        self.write("\t\t\t\t\td_y2 = abs(point2[1]-y)\n")
        self.write("\t\t\t\t\tdistances = [round(d_top,6),round(d_bottom,6),round(d_x1,6),round(d_x2,6),round(d_y1,6),round(d_y2,6)]\n")
        self.write("\t\t\t\t\ttmp = distances.count(0)\n")
        self.write("\t\t\t\t\tif tmp == 0:\n")
        self.write("\t\t\t\t\t\tcategory='mid'\n")
        self.write("\t\t\t\t\telif tmp == 1:\n")
        self.write("\t\t\t\t\t\tcategory='side'\n")
        self.write("\t\t\t\t\telse:\n")
        self.write("\t\t\t\t\t\tcategory='corner'\n")
        self.seperate_sec()
       
#Implement for after deposition as well? CHeck if historical variables are correct. Maybe all frames should be included?
    def get_temperature(self,base_depth, part_name,point1,point2):
        self.get_add_elements(part_name)
        self.get_frames()
        self.write('#GET TEMPERATURE\n')
        self.write('base_depth = ' + str(base_depth) + '\n')
        self.write('Q_z = base_depth\n')
        self.write('point1 = ' + str(point1) + '\n')
        self.write('point2 = ' + str(point2) + '\n')
        self.write('new_active_nodes = -1\n')
        self.write("dispFile = open('disp.txt','w')\n")
        #self.write("dispFile.write('#i,t,T,x,y,z,Q_x,Q_y_,Q_z,t_i,euclidean_d_Q,Q,d_top,d_bottom,d_x1,d_x2,d_y1,d_y2,category,T_1,T_2,T_3,T_4,T_5\\n')\n")
        self.get_frames()
        self.write("active_elements = []\n")
        self.write("active_nodes = []\n")
        self.write("active_time = []\n")
        self.write("frame_index = -1\n")
        self.write("for frame in frames:\n")
        self.write("\tframe_index += 1\n")
        self.write("\ttime = frame.frameValue\n")
        self.write("\tif time > 2000:\n")
        self.write("\t\traise SystemExit(0)\n")
        self.get_active_elements()
        self.write("\t#checking if deposition has ended\n")
        self.write("\tif new_active_nodes == len(active_nodes):\n")
        self.write("\t\tpass\n")
        self.write("\telse:\n")
        self.write("\t\tnew_active_nodes = len(active_nodes)\n")
        self.write("\t\ttemperature = frame.fieldOutputs['NT11']\n")
        self.write("\t\tposition = frame.fieldOutputs['COORD']\n")
        self.write("\t\t#get top of part\n")
        self.write("\t\tfor j in range(0,len(position.values)):\n")
        self.write("\t\t\tpos = position.values[j]\n")
        self.write("\t\t\tif pos.data[2] > Q_z:\n")
        self.write("\t\t\t\tQ_z = pos.data[2]\n")
        self.write("\t\tif active_nodes != []:\n")
        self.write("\t\t\tfor i in range(0,len(temperature.values)):\n")
        self.write("\t\t\t\tpos = position.values[i]\n")
        self.write("\t\t\t\ttemp = temperature.values[i]\n")
        self.write("\t\t\t\tif temp.nodeLabel in active_nodes:\n")
        self.get_historical_temperatures()
        self.write("\t\t\t\t\ti = temp.nodeLabel\n")
        self.write("\t\t\t\t\tt = time\n")
        self.write("\t\t\t\t\tt_i = active_time[active_nodes.index(temp.nodeLabel)]\n")
        self.write("\t\t\t\t\tT = temp.data\n")
        self.write("\t\t\t\t\tx = pos.data[0]\n")
        self.write("\t\t\t\t\ty = pos.data[1]\n")
        self.write("\t\t\t\t\tz = pos.data[2]\n")
        self.get_free_surface_distance()
        self.write("\t\t\t\t\tdispFile.write(str(i) + ',' + str(t) + ',' + str(T) + ',' + str(x) + ',' + str(y) + ',' + str(z) + ',,,,' + str(t_i) + ',,,'  + str(d_top) + ',' + str(d_bottom)+ ',' + str(d_x1) + ',' + str(d_x2) + ',' + str(d_y1) + ',' + str(d_y2) + ',' + category + ',' + str(hist_temp[0]) + ',' + str(hist_temp[1]) + ',' + str(hist_temp[2]) + ',' + str(hist_temp[3]) + ',' + str(hist_temp[4]) +'\\n')\n")
        self.write("dispFile.close()\n")

    def get_active_elements(self):
        self.write("#find active elements for frame\n")
        self.write("\tactive = frame.fieldOutputs['EACTIVE'].values\n")
        self.write("\tfor i in range(0,len(active)):\n")
        self.write("\t\tif active[i].data == 1.0 and active[i].elementLabel not in active_elements:\n")
        self.write("\t\t\tactive_elements.append(active[i].elementLabel)\n")
        self.write("\t\t\tfor element in add_elements:\n")
        self.write("\t\t\t\tif element.label == active[i].elementLabel:\n")
        self.write('\t\t\t\t\ttemp = element.connectivity\n')
        self.write('\t\t\t\t\tfor j in temp:\n')
        self.write('\t\t\t\t\t\tif j not in active_nodes:\n')
        self.write('\t\t\t\t\t\t\tactive_time.append(time)\n')
        self.write('\t\t\t\t\t\t\tactive_nodes.append(j)\n')
        self.seperate_sec()
        
    def get_historical_temperatures(self):
        self.write("\t\t\t\t\thist_temp = [] #to store historical temperature values\n")
        self.write("\t\t\t\t\tfor k in range(1,6):\n")
        self.write("\t\t\t\t\t\tif frame_index-k <1:\n")
        self.write("\t\t\t\t\t\t\thist_temp.append(None)\n")
        self.write("\t\t\t\t\t\telse:\n")
        self.write("\t\t\t\t\t\t\ttmp_frame = frames[frame_index-k] #fetching the frame k numbers behind the current frame\n")
        self.write("\t\t\t\t\t\t\ttmp_temperature = tmp_frame.fieldOutputs['NT11']\n")
        self.write("\t\t\t\t\t\t\ttmp_temp = tmp_temperature.values[i]\n")
        self.write("\t\t\t\t\t\t\tprint(temp.nodeLabel + tmp_temp.nodeLabel)\n")
        self.write("\t\t\t\t\t\t\thist_temp.append(tmp_temp.data)\n")


    def create_excel(self):
        workbook = xlsxwriter.Workbook('temperatures.xlsx')
        worksheet = workbook.add_worksheet()
        
    def write_excel(self, row, col, data, worksheet):
        worksheet.write(row, col, data)
        
    def end_excel(self, workbook):
        workbook.close()



