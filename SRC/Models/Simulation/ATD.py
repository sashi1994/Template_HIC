import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from constants.Directory_MME import *


class Get_ATD_Vector:
    '''
    Extraction of ATD Details
    '''
    def __init__(self, directory):
        self.directory = directory
        

    def Vector(self,r)   ->tuple:
        """
        * The function takes channel as input and return Channel's : Location, Request, Units and time series.\n
        * Example:\n
        >>> vector (Channel)
        vector[Location, Request, Units, Time History]
        """
        Data=open(r,mode='r') 
        Data= pd.DataFrame(Data)
        Location=(Data.iloc[15][0].split(":")[1])
        Request=(Data.iloc[22][0].split(":")[1])
        Units=(Data.iloc[19][0].split(":")[1])
        vector=Data.iloc[33:][0]
        return Location,Request,Units,vector

    def ATD_Get_Nodes(self)  ->pd.DataFrame:
        '''
        * Input as "Path of MME"\n
        * Returns: "Dataframe"\n
        * Time Series of ATD Nodes Coordinates (X-Y-Z) from MME\n
        '''
        os.chdir(self.directory+'\Channel')

        for file in glob.glob("*.chn"):
            Channel=str(self.directory +'/Channel'+'/'+file)
        
        ATD_Dataframe = pd.DataFrame()

        datafile = open(self.directory +'/Channel'+'/'+file).readlines() 

        for line in datafile:
            if line[29:45]=="K0TIRS000000TI00":
                Channel=self.Vector(self.directory+'/Channel'+'/'+str('2641H.'+line[16:28].strip()))
                ATD_Dataframe[str(str(Channel[0].strip())+'_'+str(Channel[1].strip())+'_('+str(Channel[2].strip())+')')]=pd.to_numeric(Channel[3])        
       
        for info in ATD_Info:
            datafile = open(self.directory +'/Channel'+'/'+file).readlines()
            for coordinates in Direction:
                for ISO in ISO_CODE_ATD:
                    for line in datafile:
                        if line[29:31]==ATD_Info[info] and line[31:35]==ISO_CODE_ATD[ISO] and line[39:41]=='HL' and line[41:43]=='CO' and line[43:44]==Direction[coordinates]:
                            Channel=self.Vector(self.directory+'\Channel'+'/'+str('2641H.'+line[16:28].strip()))
                            String=str(str(ATD_Info[info])+'_'+str(Channel[0].strip())+'_'+line[31:39]+'_'+str(Channel[1].strip())+'_('+str(Channel[2].strip())+')')
                            ATD_Dataframe[String]=pd.to_numeric(Channel[3])
                            # ATD_Dataframe[line]=pd.to_numeric(0)
                            

        return ATD_Dataframe
