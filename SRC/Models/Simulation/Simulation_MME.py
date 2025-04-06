from SRC.Models.Simulation.Read_MME import *  # Import everything from Info - ensure it's accessible
from SRC.constants.Directory_MME import *  # Import everything from Directory_MME
#from ATD import *  # Import everything from ATD
import pandas as pd

class Simulation_MME:
    """
    A class to handle and plot ATD simulation data.
    Inherits from Get_ATD_Vector to utilize vector functionalities.
    """
    
    def __init__(self,body_parts):
        """
        Initialize the Simulation_ATD instance with directory configurations.
        :param directory: An instance for directory configuration which includes data structure
        """
        self.body_parts = body_parts
         
    def check_part_exists(self, part: str):
        """
        Validate whether the specified part exists in the ATD configuration.
        :param part: The part identifier to validate.
        """
        if part not in self.body_parts:
            raise ValueError(f"Error: Part '{part}' does not exist in ATD. Available parts: {list(self.body_parts.keys())}")

    def Acceleration(self, part: str): 
        """
        Retrieve acceleration data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of acceleration data
        """
        
        self.check_part_exists(part)
        print('accel')

    def Angular_Velocity(self, part: str): 
        """
        Retrieve Angular velocity data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of acceleration data
        """
        
        self.check_part_exists(part)
        print('AV')

    def Pulse(self): 
        """
        Retrieve Pulse data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of acceleration data
        """

    def Force(self): 
        """
        Retrieve Pulse data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of acceleration data
        """
        
    
    @staticmethod
    def Vector(r)->tuple:
        """
        Extracts and returns location, request, units, and time series from a channel file.
        """
        Data=open(r,mode='r') 
        Data= pd.DataFrame(Data)
        Location=(Data.iloc[13][0].split(":")[1])
        Request=(Data.iloc[22][0].split(":")[1])
        Units=(Data.iloc[19][0].split(":")[1])
        vector=Data.iloc[33:][0]
        return Location,Request,Units,vector
