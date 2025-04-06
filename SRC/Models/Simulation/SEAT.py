import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from constants.Directory_MME import *
from ATD import *

class Seat_Vector (Get_ATD_Vector):

    def Seat_Get_Nodes(self):
        """
        * Input as "Path of MME"
        * Output: "Dataframe"
        * Time Series of Seat Nodes Coordinates (X-Y-Z) from MME

        """
        os.chdir(self.directory+'\Channel')

        for file in glob.glob("*.chn"):
            Channel=str(self.directory +'/Channel'+'/'+file)
        
        Seat_Dataframe = pd.DataFrame()

        datafile = open(self.directory +'/Channel'+'/'+file).readlines()   

        for line in datafile:
            if line[29:45]=="K0TIRS000000TI00":
                Channel=self.Vector(self.directory+'/Channel'+'/'+str('2641H.'+line[16:28].strip()))
                Seat_Dataframe[str(str(Channel[0].strip())+'_'+str(Channel[1].strip())+'_('+str(Channel[2].strip())+')')]=pd.to_numeric(Channel[3])    

        for coordinates in Direction:
            datafile = open(self.directory +'/Channel'+'/'+file).readlines()
            for info in Seat_Info:
                for ISO in ISO_CODE_SEAT:
                    for line in datafile:
                        if line[29:31]==Seat_Info[info] and line[31:36]==ISO_CODE_SEAT[ISO] and line[39:41]=='00' and line[41:43]=='CO' and line[43:44]==Direction[coordinates]:
                            Channel=Get_ATD_Vector.Vector(self, self.directory+'/Channel'+'/'+str('2641H.'+line[16:28].strip()))
                            String=str(str(Seat_Info[info])+'_'+str(Channel[0].strip())+'_'+line[31:39]+'_'+str(Channel[1].strip())+'_('+str(Channel[2].strip())+')')
                            Seat_Dataframe[String]=pd.to_numeric(Channel[3])
        return Seat_Dataframe
