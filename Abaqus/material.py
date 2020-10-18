# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 13:17:26 2020

@author: Kari Ness
"""
import os 
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns


class Material:
    def __init__(self,material_properties, material_name):
        #The material_properties should be a list of strings containing material property types
        self.material_properties = material_properties
        
        #The material should be a string
        self.material_name = material_name
        
    def get_material_name(self):
        return self.material_name
        
    def get_property_file(self, material_property):
        file_name = self.get_material_name() + '_' + material_property + '.txt'
        #file = os.path.join("C:\\Users\\kariln\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), file_name)
        file = os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), file_name)
        return file
    
    def get_property_table(self, material_property):
        file = self.get_property_file(material_property)
        table = []
        with open(file,"r") as f:
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table
    
    def plot_conductivity(self):
        material_name = self.get_material_name()
        degree_sign= u'\N{DEGREE SIGN}'
        table_conductivity = self.get_property_table('Conductivity')
        temp = [x[0] for x in table_conductivity]
        conductivity = [x[1] for x in table_conductivity]
        mpl.style.use('seaborn-dark-palette')
        plt.plot(conductivity, temp, c= 'firebrick')
        plt.xlabel('Temperature [C' + degree_sign + ']')
        plt.ylabel('Conductivity [W/m' + degree_sign + 'C]')
        plt.savefig(os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), material_name + '_Conductivity.png'))
        plt.show()
        
    def plot_specific_heat(self):
        mpl.style.use('seaborn-dark-palette')
        degree_sign= u'\N{DEGREE SIGN}'
        material_name = self.get_material_name()
        table_specific = self.get_property_table('SpecificHeat')
        temp = [x[0] for x in table_specific]
        specific_heat = [x[1] for x in table_specific]
        plt.plot(specific_heat, temp, c='firebrick')
        plt.xlabel('Temperature [C' + degree_sign + ']')
        plt.ylabel("Specific heat [J/kg" + degree_sign + 'C]')
        plt.savefig(os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), material_name + '_SpecificHeat.png'))
        plt.show()
        
    def plot_yield_stress(self):
        mpl.style.use('seaborn-dark-palette')
        degree_sign= u'\N{DEGREE SIGN}'
        material_name = self.get_material_name()
        table_yield = self.get_property_table('Plastic')
        plastic_strain = [x[1] for x in table_yield]
        yield_stress_tmp = [x[0] for x in table_yield]
        temp_tmp = [x[2] for x in table_yield]
        yield_stress = []
        temp = []
        for i in range(0,len(plastic_strain)):
            if plastic_strain[i] != 0:
                temp.append(temp_tmp[i])
                yield_stress.append(yield_stress_tmp[i])
        plt.plot(temp, yield_stress,c='firebrick')
        plt.xlabel('Temperature [C' + degree_sign + ']')
        plt.ylabel("Yield stress [MPa]")
        plt.savefig(os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), material_name + '_Yield_Stress.png'))
        plt.show()
        
    def plot_youngs_module(self):
        mpl.style.use('seaborn-dark-palette')
        degree_sign= u'\N{DEGREE SIGN}'
        material_name = self.get_material_name()
        table_E = self.get_property_table('Elastic')
        E = [x[0] for x in table_E]
        temp = [x[2] for x in table_E]
        plt.plot(temp,E, c='firebrick')
        plt.xlabel('Temperature [C' + degree_sign + ']')
        plt.ylabel("Young's Modulus [GPa]")
        plt.savefig(os.path.join("C:\\Users\\Kari Ness\\Documents\\GitHub\\Master\\Materials\\" + self.get_material_name(), material_name + '_Youngs.png'))
        plt.show()
        
    def material_plot(self):
        self.plot_conductivity()
        self.plot_yield_stress()
        self.plot_specific_heat()
        self.plot_youngs_module()


        
        
    
def main():
    AA2319 = Material([['Conductivity', 'ON'],['Density', 'OFF'],['Elastic', 'ON'],['Expansion','ON'],['LatentHeat', None],['Plastic','ON'],['SpecificHeat', 'ON']], 'AA2319')
    AA2319.material_plot()
main()