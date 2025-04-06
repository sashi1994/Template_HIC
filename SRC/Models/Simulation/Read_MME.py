import pandas as pd
from SRC.constants.Directory_MME import *  
from SRC.Models.Simulation.Get_ATD_Sled import Get_Time, Get_ATD, Get_Sled
import os
import glob

# Define a global variable
directory = None  

class Read_MME:
    '''
    Extraction of ATDs and Sleds from a given directory.
    This class reads a specific .chn file and extracts relevant ATD and Sled information.
    '''
    
    def __init__(self, dir_path):
        '''
        Initialize the MME class with the given directory.
        :param dir_path: Path to the directory containing the Channel folder.
        '''
        global directory  # Use the global directory variable
        self.directory = dir_path  # Store the directory path globally
        
    
    def Simulation_Test_info(self) -> dict:
        '''
        Extract Time, ATD and Sled information from the .chn file.
        :return: A dictionary containing ATD & Sled names as keys and extracted Time ATD & Sled objects as values.
        '''
        Test_info = {}  

        for info in Time_Info:
            
            Test_info[info] = Get_Time(info)  
            print(f"Time: {info} Channel found !!")   
        
        for info in ATD_Info:  
            Read = open(self.directory + '/Channel' + '/' + '2641H.chn').readlines()  

            Check = any(line[29:31] == ATD_Info[info] and line[39:41] == 'HH' for line in Read)

            if Check is True:
                Test_info[info] = Get_ATD(info)  
                print(f"ATD: {info} found !!")  

        for info in Sled_Info:  
            Read = open(self.directory + '/Channel' + '/' + '2641H.chn').readlines()  

            Check = any(line[29:31] == Sled_Info[info] and line[31:35] == 'SETR' for line in Read)

            if Check is True:
                Test_info[info] = Get_Sled(info)  
                print(f"SLED {info} found !!")  
                   
        return Test_info  
