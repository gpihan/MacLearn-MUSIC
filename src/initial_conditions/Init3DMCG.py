import os
import shutil
import numpy as np
import subprocess
from ..utils import *

class Init3DMCG():
    def __init__(self, Param, InitCondParam, InitPath):
        self.Parameters = InitCondParam
        self.OutputFolder = Param["OutputFolder"]
        self.parameter_path = InitPath
        self.path = "submodules/3dMCGlauber"
        self.Nev = Param["Nev"]
        self.PrepareFolder()
    
    def PrepareFolder(self):
        self.Folder_path = create_folder("OUTPUT/"+self.OutputFolder)
        self.Fname_out = self.Folder_path.split("/")[-1]
        shutil.copyfile(self.parameter_path, self.Folder_path+"/parameters.py")
        shutil.copyfile(self.path+"/input", self.Folder_path+"/input")
        os.system("ln -s "+self.path+"/3dMCGlb.e " +os.path.abspath(self.Folder_path)+"/3DMCG")
        os.system("ln -s "+self.path+"/Metropolis.e " +os.path.abspath(self.Folder_path)+"/Metropolis.e")
        os.system("ln -s "+self.path+"/tables " +os.path.abspath(self.Folder_path)+"/tables")
        return self.Folder_path, self.Fname_out
    
    def generate(self):
        """ This function generates nev initial stage
            events using 3DMCGlauber set on paraDict parameters
        """
        os.chdir(os.path.abspath(self.Folder_path))
        command = "./3DMCG {} input -1 batch_density_output=1".format(self.Nev)
        for ikey in self.Parameters.keys():
            command += " {}={}".format(ikey, self.Parameters[ikey])
        subprocess.run(command, shell = True, executable="/bin/bash")

        edArr = np.fromfile("ed_etas_distribution_N_72.dat", dtype="float32")
        nBArr = np.fromfile("nB_etas_distribution_N_72.dat", dtype="float32")
        nQArr = np.fromfile("nQ_etas_distribution_N_72.dat", dtype="float32")


        edArr = edArr.reshape(-1, 72)
        nBArr = nBArr.reshape(-1, 72)
        nQArr = nQArr.reshape(-1, 72)

        eta = nBArr[0]
        edArr = edArr[1:]
        nBArr = nBArr[1:]
        nQArr = nQArr[1:]
        os.chdir(self.path)
        return eta, edArr, nBArr, nQArr
