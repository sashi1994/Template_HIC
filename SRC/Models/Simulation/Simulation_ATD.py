# Import necessary libraries for data manipulation and plotting
import plotly.express as px
import pandas as pd
import os
import glob

# Import custom classes/modules you've developed
from Read_MME import *  # Import everything from Info - ensure it's accessible
from constants.Directory_MME import *  # Import everything from Directory_MME
from ATD import *  # Import everything from ATD

class Simulation_ATD(Get_ATD_Vector):
    """
    A class to handle and plot ATD simulation data.
    Inherits from Get_ATD_Vector to utilize vector functionalities.
    """
    
    def __init__(self, directory):
        """
        Initialize the Simulation_ATD instance with directory configurations.
        :param directory: An instance for directory configuration which includes data structure
        """
        self.mme_instance = directory
        # print(f"Number of ATDs: {self.mme_instance.NumberOfATDs}")
         
    def check_part_exists(self, part: str):
        """
        Validate whether the specified part exists in the ATD configuration.
        :param part: The part identifier to validate.
        """
        if part not in ISO_CODE_ATD:
            raise ValueError(f"Error: Part '{part}' does not exist in ATD. Available parts: {list(ISO_CODE_ATD.keys())}")

    def acceleration(self, part: str): 
        """
        Retrieve acceleration data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of acceleration data
        """
        self.check_part_exists(part)

        Acceleration_Dataframe = pd.DataFrame()
        
        # Locate and process each channel file
        for file in glob.glob("*.chn"):
            file_path = os.path.join(self.mme_instance.directory, 'Channel', file)
            datafile = open(file_path).readlines()
            
            for line in datafile:
                # Identify constant strings/data lines to extract time vector details
                if line[29:45] == "K0TIRS000000TI00":
                    channel_file = f"{self.mme_instance.directory}/Channel/2641H.{line[16:28].strip()}"
                    Channel = self.Vector(channel_file)
                    Acceleration_Dataframe[str(Channel[0].strip()) + '_' + str(Channel[1].strip()) + '_(' + str(Channel[2].strip()) + ')'] = pd.to_numeric(Channel[3])

            # Process file lines pertaining to specific ATD parts and directions
            for info in self.mme_instance.NumberOfATDs:
                for coordinates in Direction:
                    for line in datafile:
                        if (
                            line[29:31] == ATD_Info[info] 
                            and line[31:35] == ISO_CODE_ATD[part] 
                            and line[35:39] == '00'+Direction[coordinates]+Direction[coordinates]
                            and line[39:41] == 'HH'
                            and line[41:43] == 'AC' 
                            and line[43:44] == Direction[coordinates]
                        ):
                            channel_file = f"{self.mme_instance.directory}/Channel/2641H.{line[16:28].strip()}"
                            Channel = self.Vector(channel_file)
                            String = (
                                f"{ATD_Info[info]}_{Channel[0].strip()}_{line[31:39]}_{Channel[1].strip()}_({Channel[2].strip()})"
                            )
                            Acceleration_Dataframe[String] = pd.to_numeric(Channel[3])
                            
        return Acceleration_Dataframe

    def angular_velocity(self, part: str): 
        """
        Retrieve angular velocity data for a specified part.
        :param part: The specific part identifier requested from the dataset.
        :return: DataFrame of angular velocity data
        """
        self.check_part_exists(part)
        return self._create_dataframe(part, 'AV')

    def _create_dataframe(self, part: str, direction_type: str):
        """
        Helper method to build a DataFrame from channel files based on the specified part and direction type.
        :param part: The identifier of the part.
        :param direction_type: Specifies whether data is for 'AC' (acceleration) or 'AV' (angular velocity).
        :return: Populated DataFrame with parsed data.
        """
        os.chdir(self.mme_instance.directory + '\\Channel')  # Navigate to Channel directory
    