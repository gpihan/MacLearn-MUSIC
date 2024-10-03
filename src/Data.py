# This class is handling the reading and formatting of the training data.
# The input data are of two types
# 1) a dictionary containing initial B, Q, (S) and final proton, antiproton, neutrons, antineutrons, Bfinal, Qfinal, (Sfinal)
# rapidity distributions
# 2) the .h5 output files from iEBE-MUSIC (https://github.com/chunshen1987/iEBE-MUSIC) that will be converted to 1).
# 
# This class also contains a formatter to 2D numpy arrays (NumberOfEvents, Nrapidities)

from numpy import *
import sys
import h5py
import sys
import os
import pickle
from .utils import Particles
from scipy.ndimage import gaussian_filter1d
from sklearn.model_selection import train_test_split

class Data:
    def __init__(self, Param):
        self.DataPath = Param["DataPath"]
        self.setName = Param["SetName"]
        self.DataInformation = Param["DataInformation"]
        self.GaussianSmoothingSigma = Param["GaussianSmoothingSigma"]
        self.FeatureType = Param["FeaturesType"]
        self.pT_min = str(Param["pTCuttOff"][0])
        self.pT_max = str(Param["pTCuttOff"][1])
        self.pTstring = "_dNdy_pT_"+self.pT_min+"_"+self.pT_max+".dat"
        self.centralities = Param["centralities"]
        self.dataSET = []
        self.possibleNuclei = Param["PossibleNuclei"]
        self.NucEncoder = {a:i for i,a in enumerate(self.possibleNuclei)} 
        self.PossibleCharges = ["B", "Q"]
        self.TestPercentage = 0.2 #Split 20% of input data for tests
        self.IsProperlyShaped = False
        self.NumberOfFeatures = 0
        self.PossibleFeatures = self.getMetaData()

    def getMetaData(self):
        arr = array([[self.NucEncoder[data[0]], data[1]] for data in self.DataInformation])
        A = set(arr[:,0])
        B = set(arr[:,1])
        L = [a for a in A]
        for b in B:
            L.append(b)
        print(L)
        #return [list(set(arr[:,i])) for i in range(len(arr[:,0]))]
        return L

    def loadH5(self, path, Nucleus, fname):
        cen_names = [str(int(a))+"-"+str(int(b)) for a,b in zip(self.centralities[:-1], self.centralities[1:])]
        # Filename for initial distributions 
        initBfile_name = "nB_etas_distribution_N_72.dat"
        initQfile_name = "nQ_etas_distribution_N_72.dat"

        # Filename for the freeze-out densities
        FOBfile_name = "FO_nBvseta.dat"

        selected_particles = ["proton", "anti_proton", "neutron", "anti_neutron", "pion_p", "pion_m", "kaon_p", "kaon_m"]
        particles_FINAL_file_names = {particle:"particle_"+Particles[particle]+self.pTstring for particle in selected_particles}

        # reading .h5 file
        db = {}
        hf = h5py.File(path, "r")
        event_list = list(hf.keys())
        
        dataDICT = {Nucleus:{}}
        # file_name for Nch in -0.5, 0.5 for event selection
        file_name = "particle_9999_vndata_eta_-0.5_0.5.dat"
        dNdyDict = {}
        for event_name in event_list:
            event_group = hf.get(event_name)
            dNdyDict[event_name] = nan_to_num(event_group.get(file_name))[0,1]
        dNdyList = -sort(-array(list(dNdyDict.values())))

        for j, icen in enumerate(range(len(self.centralities) - 1)):
            selected_events_list = []
            if self.centralities[icen+1] < self.centralities[icen]: continue

            ihigh = int(len(dNdyList)*self.centralities[icen]/100.)
            ilow = min(len(dNdyList)-1,int(len(dNdyList)*self.centralities[icen+1]/100.))
            dN_dy_cut_high = dNdyList[ihigh]
            dN_dy_cut_low  = dNdyList[ilow]

            for event_name in dNdyDict.keys():
                if (dNdyDict[event_name] > dN_dy_cut_low and dNdyDict[event_name] <= dN_dy_cut_high):
                    selected_events_list.append(event_name)

            nev = len(selected_events_list)
            if nev == 0:
                continue
            
            

            di = {"B":{}, "Q":{}, "ap":{}, "an":{}, "p":{}, "n":{}, "netp":{}, "Npart":[]}
            BINITARR, BFOARR, BFINALARR= []
            PFINALARR, NFINALARR, APFINALARR, ANFINALARR = []
            NETPFINALARR, NETNFINALARR = [], []
            QINITARR, QFOARR, QFINALARR = []
            LNpart = []
            for i, ev in enumerate(selected_events_list):
                group = hf.get(ev)

                # read Npart
                ev_num = str(ev.split("_")[-1]) 
                string_ev = group.get("strings_"+ev_num+".dat")
                cmts = str(string_ev.attrs["header"])
                s = slice(cmts.find("Npart"), cmts.find("Ncoll")-1, 1)
                LNpart.append(float(cmts[s].split(" ")[-1]))

                # Get initial rapidity distributions

                # B
                Btemp_data = group.get(initBfile_name)
                Btemp_data = nan_to_num(Btemp_data)
                BINITARR.append(list(Btemp_data[:, 1]))
                #Q
                Qtemp_data = group.get(initQfile_name)
                Qtemp_data = nan_to_num(Qtemp_data)
                QINITARR.append(list(Qtemp_data[:, 1]))

                # Get freeze-out rapidity distributions

                # B
                BFO_data = group.get(FOBfile_name)
                BFO_data = nan_to_num(BFO_data)
                BFOARR.append(list(BFO_data[:, 1]))

                # Q
                QFO_data = group.get(FOBfile_name)
                QFO_data = nan_to_num(QFO_data)
                QFOARR.append(list(BFO_data[:, 2])) # Q is at position 2 in FO_nBvseta.dat file

                # Get final rapidity distributions

                part = {}
                for partnam, filnam in particles_FINAL_file_names.items():
                    temp =  group.get(filnam)
                    temp =  nan_to_num(temp)
                    part[partnam] = temp[:,1]
                py = part["proton"]
                ny = part["neutron"]

                apy = part["anti_proton"]
                any = part["anti_neutron"]

                Nnpy = part["proton"] - part["anti_proton"]
                Nnny = part["neutron"] - part["anti_neutron"]

                NBy = part["proton"] - part["anti_proton"] + part["neutron"] - part["anti_neutron"]
                NQy = part["proton"] - part["anti_proton"] + part["pion_p"] - part["pion_m"] + part["kaon_p"] - part["kaon_m"]

                # get eta init and final only once (from protons) 
                if i == 0 and j == 0:
                    temp = group.get("particle_2212_dNdy_pT_0.2_3.dat")
                    temp =  nan_to_num(temp)
                    # Same for both B and Q
                    db["INITIAL_eta"] = Btemp_data[:, 0]
                    db["FINAL_eta"] = array(temp[:,0])
                    db["FO_eta"] = BFO_data[:,0]

                BFINALARR.append(NBy)
                PFINALARR.append(py)
                NFINALARR.append(ny)
                ANFINALARR.append(any)
                APFINALARR.append(apy)
                NETPFINALARR.append(Nnpy)
                NETNFINALARR.append(Nnny)
                QFINALARR.append(NQy)

            LNpart = array(LNpart)
            di["Npart"] = LNpart
            BINITARR = array(BINITARR)
            BFOARR = array(BFOARR)
            BFINALARR = array(BFINALARR)

            PFINALARR = array(PFINALARR)
            NFINALARR = array(NFINALARR)
            APFINALARR = array(APFINALARR)
            ANFINALARR = array(ANFINALARR)
            NETPFINALARR = array(NETPFINALARR)
            NETNFINALARR = array(NETNFINALARR)

            QINITARR = array(QINITARR)
            QFOARR = array(QFOARR)
            QFINALARR = array(QFINALARR)

            di["B"]["INITIAL"] = BINITARR
            di["Q"]["INITIAL"] = QINITARR

            di["B"]["FO"] = BFOARR
            di["Q"]["FO"] = QFOARR

            di["B"]["FINAL"] = BFINALARR
            di["Q"]["FINAL"] = QFINALARR
            di["p"]["FINAL"] = PFINALARR
            di["n"]["FINAL"] = NFINALARR
            di["ap"]["FINAL"] = APFINALARR
            di["an"]["FINAL"] = ANFINALARR
            di["netp"]["FINAL"] = NETPFINALARR
            di["netn"]["FINAL"] = NETNFINALARR

            db[cen_names[icen]] = di
        dataDICT[Nucleus] = db
        # Write the dictionary not to lost it
        fi = open(fname+"_dict.dat", 'wb')
        pickle.dump(dataDICT, fi)
        fi.close()
        return dataDICT 

    def checkNuc(self, fname):
        for PossibleNucleus in self.possibleNucleis:
            if PossibleNucleus in fname:
                return PossibleNucleus
        
    def load_data(self):
        # This method reads all the data in each data path
        # if data is .h5, convert in dictionnary and pickle object first (requires names to contain nucleus)
        # if data is .dat, assumes its pickle object with 
        # the data.
        h, _, files = next(os.walk(self.DataPath))
        self.lenDataPath = len(files)
        for fi in files:
            fpath = h+"/"+fi
            if os.path.splitext(fi) == ".h5":
                Nucleus = self.checkNuc(fi)
                self.dataSET.append(self.loadH5(fpath, Nucleus, fi))
            else:
                try:
                    with open(fpath, "rb") as pf:
                        self.dataSET.append(pickle.load(pf))
                except FileNotFoundError:
                    print("Training dictionary not found.")
                    sys.exit()
    
    def load(self, Dct, Nuc, cent, charge):
        Yin = Dct[Nuc][cent][charge]["INITIAL"]
        Yfin = Dct[Nuc][cent][charge]["FINAL"]
        Yfin_netp = Dct[Nuc][cent]['netp']["FINAL"]
        Yfin_netn = Dct[Nuc][cent]['netn']["FINAL"]
        Yfin_p = Dct[Nuc][cent]['p']["FINAL"]
        Yfin_n = Dct[Nuc][cent]['n']["FINAL"]
        return [Yin, Yfin, Yfin_netp, Yfin_netn, Yfin_p, Yfin_n]

    def loadEtas(self, Dct):
        Xin = Dct[list(Dct.keys())[0]]["INITIAL_eta"] 
        Xfin = Dct[list(Dct.keys())[0]]["FINAL_eta"] 
        return Xin, Xfin

    def AddFeatures(self, Arr, Info):
        if self.FeatureType > 3 or self.FeatureType < 0:
            print("Warning: feature type not recognized")
            self.FeatureType = 0
        if self.lenDataPath != len(self.DataInformation):
            self.FeatureType = 0
        match self.FeatureType:
            case 0:
                self.NumberOfFeatures = 0
                return Arr
            case 1:
                self.NumberOfFeatures = 1
                extra_column = self.NucEncoder[Info[0]]
                return hstack((Arr, full((Arr.shape[0], 1), extra_column)))
            case 2:
                self.NumberOfFeatures = 1
                extra_column = Info[1]
                return hstack((Arr, full((Arr.shape[0], 1), extra_column)))
            case 3:
                self.NumberOfFeatures = 2
                extra_column1 = self.NucEncoder[Info[0]]
                extra_column2 = Info[1]
                ArrTemp = hstack((Arr, full((Arr.shape[0], 1), extra_column1)))
                return hstack((ArrTemp, full((ArrTemp.shape[0], 1), extra_column2)))

    def PrepareTrainingData(self):
        # Initialize dictionary to store data for charges 'B' and 'Q'
        self.PreparedTrainingDataDict = {'B': {'Init': [], 'B': [], 'NetProton': [], 
                                                'NetNeutron': [], 'Protons': [], 'Neutrons': []},
                                        'Q': {'Init': [], 'Q': [], 'NetProton': [], 
                                            'NetNeutron': [], 'Protons': [], 'Neutrons': []}
        }
        # Iterate through the dictionaries
        for Data, DataInfo in zip(self.dataSET, self.DataInformation):
            for Nuc, cent_dict in Data.items():
                for cent, charge_dict in cent_dict.items():
                    if isinstance(charge_dict, dict):
                        for charge, data_dict in charge_dict.items():
                            if isinstance(data_dict, dict) and "INITIAL" in data_dict and "FINAL" in data_dict:
                                # Load Xin, Yin, Xfin, Yfin using the load function
                                Outlist = self.load(Data, Nuc, cent, charge)
                                
                                
                                # Add features for training data classification.
                                Outlist[0] = self.AddFeatures(Outlist[0], DataInfo)
                                #print("yolo", [len(a) for a in Outlist])
                                
                                
                                # Append data based on charge
                                for charge in self.PreparedTrainingDataDict.keys():
                                    for outType, out in zip(self.PreparedTrainingDataDict[charge].keys(), Outlist):
                                        self.PreparedTrainingDataDict[charge][outType].append(out)
        # Convert lists to numpy arrays for both charges
        
        for charge in self.PreparedTrainingDataDict.keys():
            for key in self.PreparedTrainingDataDict[charge].keys():
                self.PreparedTrainingDataDict[charge][key] = concatenate(self.PreparedTrainingDataDict[charge][key], axis=0)

    def SplitTrainingData(self, OutData, charge):
            return list(train_test_split(self.PreparedTrainingDataDict[charge]["Init"], OutData, 
                                         test_size=self.TestPercentage, random_state=42, shuffle=True))

    def PerformSplitGaussianSmoothing(self):
        self.SplitTrainedData = {'B': {'B': {"Train":[], "Test":[]}, 
                                       'NetProton': {"Train":[], "Test":[]}, 
                                        'NetNeutron': {"Train":[], "Test":[]},
                                        'Protons': {"Train":[], "Test":[]},
                                        'Neutrons': {"Train":[], "Test":[]}},
                                'Q': {'Q': {"Train":[], "Test":[]}, 
                                      'NetProton': {"Train":[], "Test":[]}, 
                                       'NetNeutron': {"Train":[], "Test":[]}, 
                                       'Protons': {"Train":[], "Test":[]}, 
                                       'Neutrons': {"Train":[], "Test":[]}}
                                }
        for charge in self.PossibleCharges:
            for OutType in self.SplitTrainedData[charge].keys():
                Xtrain, Xtest, Ytrain, Ytest = self.SplitTrainingData(self.PreparedTrainingDataDict[charge][OutType], charge)
                Ytrain, Ytest = self.apply_smoothing(Ytrain, Ytest)
                self.SplitTrainedData[charge][OutType]["Train"] = [Xtrain, Ytrain]
                self.SplitTrainedData[charge][OutType]["Test"] = [Xtest, Ytest]
        self.IsProperlyShaped = True

    def apply_smoothing(self, Ytrain, Ytest):
        Ytrain_out = [gaussian_filter1d(y, self.GaussianSmoothingSigma) for y in Ytrain]
        Ytest_out = [gaussian_filter1d(y, self.GaussianSmoothingSigma) for y in Ytest]
        return array(Ytrain_out), array(Ytest_out)
