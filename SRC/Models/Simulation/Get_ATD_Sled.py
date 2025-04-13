# Import required modules
from SRC.Models.Simulation.Simulation_MME import *      # Import everything from Simulation_MME module
from SRC.constants.Directory_MME import *               # Import everything from Directory_MME module
from SRC.Models.Simulation.Read_MME import *            # Import everything from Read_MME module
import pandas as pd                                     # Import pandas for data manipulation
import os                                               # Import os for operating system dependent functionality
import glob                                             # Import glob for file pattern matching

# ------------------------------ Class for Time Handling ------------------------------

class Get_Time:
    def __init__(self, Time_ID,directory):
        """
        Initialize Get_Time with a specific Time_ID.
        This class is responsible for retrieving and processing time series data.
        """
        try:
            # Retrieve the ID from the Time_Info dictionary
            self.ID = Time_Info[Time_ID]
            self.directory=directory
        except KeyError:
            # Raise an error if the Time ID is not found
            raise ValueError(f"Error: The Time ID '{Time_ID}' does not exist in Time_Info.")
    
    def timeseries(self) -> pd:
        """
        Calculate the timeseries for a simulation.
        :return: DataFrame containing the processed acceleration data.
        """

        # Change to the specified directory
        os.chdir(self.directory)

        # Initialize a DataFrame to store the ATD data
        Dataframe = pd.DataFrame()

        # Process each .chn file in the directory
        for file in glob.glob("*.chn"):
            channel_path = os.path.join(self.directory, file)

            # Read the channel file
            with open(channel_path) as f:
                datafile = f.readlines()
            
            for line in datafile:
                # Extract time vector details
                if line[29:45] == "K0"+self.ID+"000000TI00":
                    channel_file = os.path.join(self.directory, f"2641H.{line[16:28].strip()}")
                    
                    # Call Vector static method from Simulation_MME
                    Channel = Simulation_MME.Vector(channel_file)
                    col_name = f"{Channel[0].strip()}_({Channel[2].strip()})"
                    Dataframe[col_name] = pd.to_numeric(Channel[3])
        
        return Dataframe


# ------------------------------ Class for ATD Handling ------------------------------

class Get_ATD(Simulation_MME):
    def __init__(self, ATD_ID,directory):
        """
        Initialize Get_ATD with a specific ATD_ID.
        This class is used to retrieve and process data related to the ATD (Anthropomorphic Test Dummy).
        """
        try:
            # Retrieve the ID from the ATD_Info dictionary
            self.ID = ATD_Info[ATD_ID]
            self.body_parts = {'Head', 'Chest', 'Pelvis'}
            self.directory=directory

        except KeyError:
            # Raise an error if the ATD ID is not found
            raise ValueError(f"Error: The ATD ID '{ATD_ID}' does not exist in ISO_CODE_ATD.")
        
        # Call the parent class initialization
        super().__init__(self.body_parts)
    
    def Acceleration(self, part: str) -> pd:
        """
        Calculate acceleration for a specific part of the ATD.
        :param part: Part of the ATD to calculate the acceleration for.
        :return: DataFrame containing the processed acceleration data.
        """
        # Ensure the specified part exists
        self.check_part_exists(part)

        # Change to the specified directory
        os.chdir(self.directory)

        # Initialize a DataFrame to store the ATD data
        ATD_Dataframe = pd.DataFrame()

        # Process each .chn file in the directory
        for file in glob.glob("*.chn"):
            channel_path = os.path.join(self.directory, file)

            # Read the channel file
            with open(channel_path) as f:
                datafile = f.readlines()
            
            # Process details relating to specific ATD parts and directions
            for coordinates in Direction:
                for line in datafile:
                    if (
                        line[29:31] == self.ID and
                        line[31:35] == ISO_CODE_ATD[part] and
                        line[35:39] == '00' + Direction[coordinates] + Direction[coordinates] and
                        line[39:41] == 'HH' and
                        line[41:43] == 'AC' and
                        line[43:44] == Direction[coordinates]
                    ):
                        channel_file = os.path.join(self.directory, f"2641H.{line[16:28].strip()}")
                        Channel = Simulation_MME.Vector(channel_file)
                        String = f"{Channel[0].strip()}_({Channel[2].strip()})"
                        ATD_Dataframe[String] = pd.to_numeric(Channel[3])
                        
        return ATD_Dataframe
        
    def Angular_Velocity(self, part: str) -> pd:
        """
        Calculate Angular Velocity for a specific part of the ATD.
        :param part: Part of the ATD to calculate the angular velocity for.
        :return: DataFrame containing the processed angular velocity data.
        """
        # Ensure the specified part exists
        self.check_part_exists(part)

        # Change to the specified directory
        os.chdir(self.directory)

        # Initialize a DataFrame to store the ATD data
        ATD_Dataframe = pd.DataFrame()

        # Process each .chn file in the directory
        for file in glob.glob("*.chn"):
            channel_path = os.path.join(self.directory, file)

            # Read the channel file
            with open(channel_path) as f:
                datafile = f.readlines()

            # Process details relating to specific ATD parts and directions
            for coordinates in Direction:
                for line in datafile:
                    if (
                        line[29:31] == self.ID and
                        line[31:35] == ISO_CODE_ATD[part] and
                        line[35:39] == '0000' and
                        line[39:41] == 'HH' and
                        line[41:43] == 'AV' and
                        line[43:44] == Direction[coordinates]
                    ):
                        channel_file = os.path.join(self.directory, f"2641H.{line[16:28].strip()}")
                        Channel = Simulation_MME.Vector(channel_file)
                        String = f"{Channel[0].strip()}_({Channel[2].strip()})"
                        ATD_Dataframe[String] = pd.to_numeric(Channel[3])
                        
        return ATD_Dataframe


# ------------------------------ Class for Sled Handling ------------------------------

class Get_Sled(Simulation_MME):
    def __init__(self, Sled_ID,directory):
        """
        Initialize Get_Sled with a specific Sled_ID.
        This class is used to retrieve and process data related to the sled in the simulation.
        """
        try:
            # Retrieve the ID from the Sled_Info dictionary
            self.ID = Sled_Info[Sled_ID]
            self.body_parts = {'Base'}
            self.directory=directory
        except KeyError:
            # Raise an error if the Sled ID is not found
            raise ValueError(f"Error: The Sled ID '{Sled_ID}' does not exist in Sled_Info.")
        
        # Call the parent class initialization
        super().__init__(self.body_parts)

    def Pulse(self) -> pd:
        """
        Calculate Pulse for the sled.
        :return: DataFrame containing the processed pulse data.
        """

        # Change to the specified directory
        os.chdir(self.directory)

        # Initialize a DataFrame to store the sled data
        Sled_Dataframe = pd.DataFrame()

        # Process each .chn file in the directory
        for file in glob.glob("*.chn"):
            channel_path = os.path.join(self.directory, file)

            # Read the channel file
            with open(channel_path) as f:
                datafile = f.readlines()

            # Process details relating to specific sled parts and directions
            for line in datafile:
                if (
                    line[29:31] == 'K0' and
                    line[31:35] == 'SLED' and
                    line[35:39] == '0000' and
                    line[39:41] == '00' and
                    line[41:43] == 'AC' and
                    line[43:44] == Direction['X-Coordinate']
                ):
                    channel_file = os.path.join(self.directory, f"2641H.{line[16:28].strip()}")
                    Channel = Simulation_MME.Vector(channel_file)
                    String = f"{Channel[0].strip()}_({Channel[2].strip()})"
                    Sled_Dataframe[String] = pd.to_numeric(Channel[3])
                        
        return Sled_Dataframe

    def Force(self, part: str) -> pd:
        """
        Calculate Force for a specific part of the sled.
        :param part: Part of the sled to calculate the force for.
        :return: DataFrame containing the processed force data.
        """
        # Ensure the specified part exists
        self.check_part_exists(part)

        # Change to the specified directory
        os.chdir(self.directory)

        # Initialize a DataFrame to store the sled data
        Sled_Dataframe = pd.DataFrame()

        # Process each .chn file in the directory
        for file in glob.glob("*.chn"):
            channel_path = os.path.join(self.directory, file)

            # Read the channel file
            with open(channel_path) as f:
                datafile = f.readlines()

            # Process details relating to specific sled parts and directions
            for coordinates in Direction:
                for line in datafile:
                    if (
                        line[29:31] == self.ID and
                        line[31:35] == ISO_CODE_SLED[part] and
                        line[41:43] == 'FO' and
                        line[43:44] == Direction[coordinates]
                    ):
                        channel_file = os.path.join(self.directory, f"2641H.{line[16:28].strip()}")
                        Channel = Simulation_MME.Vector(channel_file)
                        String = f"{Channel[0].strip()}_({Channel[2].strip()})"
                        Sled_Dataframe[String] = pd.to_numeric(Channel[3])
                        
        return Sled_Dataframe