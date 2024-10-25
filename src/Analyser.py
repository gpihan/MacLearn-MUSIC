# This class contains all analysis functions
# 1) Analysis for training models performance.
# 2) Analysis on the predicted curves.
import numpy as np
from scipy.integrate import simpson
from collections import defaultdict



class Analyser():

    def __init__(self, Param):
        self.AnalysisMode = Param["AnalysisMode"]
        self.AnalysisOnTrain = Param["AnalysisOnTrain"]
        self.AnalysisOnPred = Param["AnalysisOnPred"]
        self.DoPlots = Param["DoPlots"]
        self.ChargeIn = Param["InputCharge"]
        self.ChargeOut = Param["OutputCharge"]
        self.TrainTestDict = {}


    def loadAnalysis(self, D):
        self.D = D
        if self.AnalysisMode == 1:
            if isinstance(self.AnalysisOnTrain, str):
                self.AnalysisOnTrain = [self.AnalysisOnTrain]
            self.TrainFunc = list(set(self.AnalysisOnTrain) & set(list(self.D.keys())))
            self.PredFunc = list(set(self.AnalysisOnPred) & set(list(self.D.keys())))
        else:
            self.TrainFunc = []
            self.PredFunc = []

    def PerformAnalysis(self, model, TrainingData, D):
        self.EtaIn, self.EtaOut = TrainingData.loadEtas()
        if self.AnalysisMode == 1:
            Nfeatures = TrainingData.NumberOfFeatures
            Xtest, Ytest = tuple(TrainingData.SplitTrainedData[self.ChargeIn][self.ChargeOut]["Test"])
            CTest = TrainingData.SplitTrainedData["Centralities"]["Test"]

            Ypred = model.predictOntest(Xtest)
            Xtest = np.array(Xtest)
            Ytest = np.array(Ytest)
            Ypred = np.array(Ypred)
            for func in self.TrainFunc:
                self.TrainTestDict[func] = self.D[func](self, Xtest, Ytest, Ypred, CTest)
        else:
            self.TrainTestDict = {}

    
    def ComputeMidRap(self, Arr, y1=-0.5, y2=0.5):
        i1 = np.argmin(np.abs(self.EtaOut - y1))
        i2 = np.argmin(np.abs(self.EtaOut - y2))
        midRapArr = np.mean(Arr[:,i1:i2], axis=1)
        return midRapArr

    def ComputeRMSArray(self, A):
        return np.sqrt(np.sum(A**2, axis=0)/len(A[:,0]))

    def ComputeRMS(self, X):
        return np.sqrt(np.sum(X**2)/len(X))

    def ComputeIntegralArray(self, Arr):
        return simpson(Arr, self.EtaOut, axis=1) 

    def ComputeIntegral(self, Y):
        return simpson(Y, self.EtaOut)

    def GetCentralityIndices(self, CENT):
        CentralityDict = defaultdict(list)
        for i, centrality in enumerate(CENT):
            CentralityDict[centrality].append(i)
        return CentralityDict

    def ComputeRMSDiff(self, Xtest, Ytest, Ypred, CTest):
        D = {}
        Y = Ytest-Ypred
        D["X"] = self.EtaOut
        D["Y"] = self.ComputeRMSArray(Y) 
        return D 

    def ComputeRMSDiffCentrality(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:{"X":self.EtaOut, "Y":self.ComputeRMSArray(Ytest[indexes] - Ypred[indexes])} for centr, indexes in IndexDict.items()}

    def ComputeMidRapidityRMSDiff(self, Xtest, Ytest, Ypred, CTest):
        MidRapTest = self.ComputeMidRap(Ytest)
        MidRapPred = self.ComputeMidRap(Ypred)
        return self.ComputeRMS(MidRapTest - MidRapPred)

    def ComputeGlobalChargeDiff(self, Xtest, Ytest, Ypred, CTest):
        IntegTest = self.computeIntegralArray(Ytest)
        IntegPred = self.computeIntegralArray(Ypred)
        return self.computeRMS(IntegTest - IntegPred)

    def GetRaw(self, Xtest, Ytest, Ypred, CTest):
        return {"Eta":self.EtaOut, "Xtest":Xtest, "Ytest":Ytest, "Ypred":Ypred, "Centralities":CTest}


    def Full(self, Xtest, Ytest, Ypred, CTest):
        return {
                "ComputeRMSDiff":self.ComputeRMSDiff(Xtest, Ytest, Ypred, CTest), 
                "ComputeMidRapidityRMSDiff":self.ComputeMidRapidityRMSDiff(Xtest, Ytest, Ypred, CTest), 
                "ComputeGlobalChargeDiff":self.ComputeRMSDiff(Xtest, Ytest, Ypred, CTest), 
                "ComputeRMSDiffCentrality":self.ComputeRMSDiffCentrality(Xtest, Ytest, Ypred, CTest),
                "GetRaw":self.GetRaw(Xtest, Ytest, Ypred, CTest), 
                }

    def Light(self, Xtest, Ytest, Ypred, CTest):
        return {"ComputeRMSDiff":self.ComputeRMSDiff(Xtest, Ytest, Ypred, CTest)}

    def Raw(self, Xtest, Ytest, Ypred, CTest):
        return {"GetRaw":self.GetRaw(Xtest, Ytest, Ypred, CTest)}


