# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:08:34 2020

@author: kariln
"""

from pathlib import Path
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker

class Experiment:
    def __init__(self, exp_name, folder_name):
        self.exp_name = exp_name
        self.folder_name = folder_name

    def get_folder_name(self):
        return self.folder_name
    
    def get_exp_name(self):
        return self.exp_name
    
    def get_corner_file_path(self):
        exp_name = self.get_exp_name()
        foldername = self.get_folder_name()
        file_name = 'corner_node_'+exp_name + '.txt'
        file = os.path.join(os.path.dirname(os.path.abspath(__file__ )),"exp", foldername, file_name)
        return file
    
    def get_mid_file_path(self):
        exp_name = self.get_exp_name()
        foldername = self.get_folder_name()
        file_name = 'mid_node_'+exp_name + '.txt'
        file = os.path.join(os.path.dirname(os.path.abspath(__file__ )),"exp", foldername, file_name)
        return file
    
    def get_node_data(self, node_type):
        if node_type == 'corner':
            file_path = self.get_corner_file_path()
        elif node_type == 'mid':
            file_path = self.get_mid_file_path()
            
        else:
            raise Exception('not implemented')
        table = []
        with open(file_path, "r") as f: 
            for line in f:
                tmp = line.strip().split(",")
                for i in range(0,len(tmp)):
                    tmp[i] = float(tmp[i])
                tmp = tuple(tmp)
                table.append(tmp)
        return table
    
def time_normalize_data(table):
    time_offset = table[0][0]
    return time_offset
        
def main():
    zigzag = Experiment('zigzag','exp3')
    zigzag_corner = zigzag.get_node_data('corner')
    zigzag_mid = zigzag.get_node_data('mid')
    time_offset = time_normalize_data(zigzag_mid)
    t_zigzag_mid = [x[0] for x in zigzag_mid]
    temp_zigzag_mid = [x[1] for x in zigzag_mid]
    t_zigzag_corner = [x[0] for x in zigzag_corner]
    temp_zigzag_corner = [x[1] for x in zigzag_corner]
    
    
    raster = Experiment('raster','exp2')
    raster_corner = raster.get_node_data('corner')
    t_raster_corner = [x[0] for x in raster_corner]
    temp_raster_corner = [x[1] for x in raster_corner]
    raster_mid = raster.get_node_data('mid')
    time_offset = time_normalize_data(raster_mid)
    t_raster_mid = [x[0]-time_offset for x in raster_mid]
    temp_raster_mid = [x[1] for x in raster_mid]

    degree_sign= u'\N{DEGREE SIGN}'
    # mpl.style.use('seaborn-dark-palette')
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Layer', 'Base'])
    # axes = plt.gca()
    # axes.set_xlim([0,1000])
    # #axes.set_ylim([0,800])
    # plt.savefig('midnode_zigzag_layer_base', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Layer', 'Base'])
    # axes = plt.gca()
    # axes.set_xlim([40,80])
    # #axes.set_ylim([0,800])
    # plt.savefig('midnode_zigzag_layer_base_detail', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Layer', 'Base'])
    # axes = plt.gca()
    # axes.set_xlim([52,54])
    # #axes.set_ylim([0,800])
    # plt.axvline(x=52.8215,color='r')
    # plt.savefig('midnode_zigzag_layer_base_detail2', bbox_inches = "tight")
    # plt.show()
    
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,2.5])
    # #axes.set_ylim([0,1550])
    # # tick_spacing = 0.2
    # # axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # # plt.grid()
    # plt.savefig('midnode_zigzag_1', bbox_inches = "tight")
    # plt.show()
    

    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['zigzag','raster'])
    # axes = plt.gca()
    # axes.set_xlim([300,500])
    # axes.set_ylim([260,350])
    # plt.savefig('cornernode_layer4')
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,2000])
    # #axes.set_ylim([0,800])
    # plt.savefig('midnode_zigzag')
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,500])
    # axes.set_ylim([0,800])
    # plt.savefig('midnode_zigzag_b')
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,1.0])
    # #axes.set_ylim([0,1550])
    # tick_spacing = 0.1
    # axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # plt.grid()
    # plt.savefig('midnode_zigzag_1', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,50])
    # #axes.set_ylim([0,1550])
    # plt.savefig('midnode_zigzag_1b', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([80,180])
    # axes.set_ylim([0,800])
    # plt.savefig('midnode_zigzag_2')
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([180,280])
    # axes.set_ylim([0,650])
    # plt.savefig('midnode_zigzag_3')
    # plt.show()
    
    # plt.plot(t_zigzag_corner,temp_zigzag_corner)
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([280,380])
    # axes.set_ylim([0,650])
    # plt.savefig('midnode_zigzag_4')
    # plt.show()
    import seaborn as sns
    sns.set_palette("viridis")
    plt.rcParams["figure.figsize"] = (10,3)
    plt.plot(t_raster_corner,temp_raster_corner, label = 'Corner')
    plt.plot(t_raster_mid,temp_raster_mid, color = 'cornflowerblue', label = 'Mid')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C' + degree_sign + ']')
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([-10,1000])
    axes.set_ylim([0,800])
    plt.savefig('midnode_raster')
    plt.show()

    plt.plot(t_raster_corner,temp_raster_corner, label = 'Corner')
    plt.plot(t_raster_mid,temp_raster_mid, color = 'cornflowerblue', label = 'Mid')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C' + degree_sign + ']')
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([-10,400])
    axes.set_ylim([0,800])
    plt.savefig('midnode_raster_b')
    plt.show()

    plt.rcParams["figure.figsize"] = (10,3)
    plt.plot(t_zigzag_mid,temp_zigzag_mid, label = 'Zigzag')
    plt.plot(t_raster_mid,temp_raster_mid, color = 'cornflowerblue', label = 'Raster')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C' + degree_sign + ']')
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([-10,1000])
    axes.set_ylim([0,800])
    plt.savefig('midnode_raster')
    plt.show()

    plt.plot(t_zigzag_mid,temp_zigzag_mid, label = 'Zigzag')
    plt.plot(t_raster_mid,temp_raster_mid, color = 'cornflowerblue', label = 'Raster')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C' + degree_sign + ']')
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([-10,400])
    axes.set_ylim([0,800])
    plt.savefig('midnode_raster_b')
    plt.show()
    
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.plot(t_raster_mid,temp_raster_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,2.5])
    # #axes.set_ylim([0,800])
    # plt.savefig('midnode_raster_c')
    # plt.show()
    
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.plot(t_raster_mid,temp_raster_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,50])
    # axes.set_ylim([0,800])
    # plt.savefig('midnode_raster_1')
    # plt.show()
    
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.plot(t_raster_mid,temp_raster_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([50,150])
    # axes.set_ylim([0,700])
    # plt.savefig('midnode_raster_2')
    # plt.show()
    
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.plot(t_raster_mid,temp_raster_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([150,250])
    # axes.set_ylim([0,600])
    # plt.savefig('midnode_raster_3')
    # plt.show()
    
    # plt.plot(t_raster_corner,temp_raster_corner)
    # plt.plot(t_raster_mid,temp_raster_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Corner','Mid'])
    # axes = plt.gca()
    # axes.set_xlim([300,400])
    # axes.set_ylim([0,600])
    # plt.savefig('midnode_raster_4')
    # plt.show()
    
    # zigzag_one_layer = Experiment('zigzag','One layer')
    # zigzag_one_layer_mid = zigzag_one_layer.get_node_data('mid')
    # time_offset = time_normalize_data(zigzag_one_layer_mid)
    # t_zigzag_mid = [x[0]-time_offset for x in zigzag_one_layer_mid]
    # temp_zigzag_mid = [x[1] for x in zigzag_one_layer_mid]
    
    # degree_sign= u'\N{DEGREE SIGN}'
    # mpl.style.use('seaborn-dark-palette')
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,50])
    # #axes.set_ylim([0,600])
    # plt.savefig('zigzag_one_layer_total', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,2.5])
    # #axes.set_ylim([0,600])
    # plt.savefig('zigzag_one_layer_firs_pass', bbox_inches = "tight")
    # plt.show()
    
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([0,0.2])
    # #axes.set_ylim([0,600])
    # tick_spacing = 0.1
    # axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # plt.grid()
    # plt.savefig('zigzag_one_layer_firs_pass_grid', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([5,15])
    # #axes.set_ylim([0,600])
    # plt.savefig('zigzag_one_layer_second_pass', bbox_inches = "tight")
    # plt.show()
    
    # plt.plot(t_zigzag_mid,temp_zigzag_mid)
    # plt.xlabel('Time [s]')
    # plt.ylabel('Temperature [C' + degree_sign + ']')
    # plt.legend(['Mid'])
    # axes = plt.gca()
    # axes.set_xlim([15,25])
    # axes.set_ylim([100,300])
    # plt.savefig('zigzag_one_layer_third_pass', bbox_inches = "tight")
    # plt.show()

    


main()