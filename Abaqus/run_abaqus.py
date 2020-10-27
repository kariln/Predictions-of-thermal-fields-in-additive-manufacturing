# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:01:35 2020

@author: Kari Ness
"""
import subprocess as sp
from pathlib import Path
# abaqus_path = "C:\\SIMULIA\\Commands\\abaqus.cmd"
#script_path = "C:\\Users\\Kari Ness\\Documents\\GitHub\\TKT4550---Structural-Engineering-Specialization-Project\\Abaqus\\create_part.py"
# sp.call([abaqus_path, 'cae', "noGUI=C:\\temp\\create_part.py"],shell = True)
script_path = Path('scripted_part.py')
p = 'C:\\Users\\kariln\\Documents\\GitHub\\Master\\Abaqus'
#pythonFilePath = "C:\\Temp\\DirectoryWithThePythonScript\\"
sp.call(['abaqus.bat', 'python', p, 'scripted_part.py'])