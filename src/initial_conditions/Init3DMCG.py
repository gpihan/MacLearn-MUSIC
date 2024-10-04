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

    ## To generalize to different init cond
    
    def PrepareFolder(self):
        self.Folder_path = create_folder("OUTPUT/"+self.OutputFolder)
        self.Fname_out = self.Folder_path.split("/")[-1]
        shutil.copyfile(self.parameter_path, self.Folder_path+"/input3dMCG_default.py")
        shutil.copyfile(self.path+"/input", self.Folder_path+"/input")
        os.system("ln -s "+os.path.abspath(self.path+"/3dMCGlb.e") + " " +os.path.abspath(self.Folder_path)+"/3DMCG")
        os.system("ln -s "+os.path.abspath(self.path+"/Metropolis.e") + " " +os.path.abspath(self.Folder_path)+"/Metropolis.e")
        os.system("ln -s "+os.path.abspath(self.path+"/tables") + " " +os.path.abspath(self.Folder_path)+"/tables")
        return self.Folder_path, self.Fname_out
    
    def read(self, path="", N=72):
        if path == "":
            PATH = ""
        else:
            PATH = path.rstrip("/")+"/"
        edArr = np.fromfile(PATH+"ed_etas_distribution_N_72.dat", dtype="float32").reshape(-1, N)
        nBArr = np.fromfile(PATH+"nB_etas_distribution_N_72.dat", dtype="float32").reshape(-1, N)
        nQArr = np.fromfile(PATH+"nQ_etas_distribution_N_72.dat", dtype="float32").reshape(-1, N)
        return nBArr[0], edArr[1:], nBArr[1:], nQArr[1:]


    def generate(self):
        """ This function generates nev initial stage
            events using 3DMCGlauber set on paraDict parameters
        """
        h = os.getcwd()
        os.chdir(os.path.abspath(self.Folder_path))
        command = "./3DMCG {} input -1 batch_density_output=1".format(self.Nev)
        for ikey in self.Parameters.keys():
            command += " {}={}".format(ikey, self.Parameters[ikey])
        subprocess.run(command, shell = True, executable="/bin/bash")
        eta, edArr, nBArr, nQArr = self.read()
        os.chdir(h)
        return eta, edArr, nBArr, nQArr
