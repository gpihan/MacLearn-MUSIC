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

    
    def ComputeIntegralArray(self, Arr):
        return simpson(Arr, x=self.EtaOut, axis=1) 

    def GetCentralityIndices(self, CENT):
        CentralityDict = defaultdict(list)
        for i, centrality in enumerate(CENT):
            CentralityDict[centrality].append(i)
        return CentralityDict

    def global_charge(self, Ypred, Ytest):
        IntPred = self.ComputeIntegralArray(Ypred)
        IntTest = self.ComputeIntegralArray(Ytest)
        return np.array(IntPred) - np.array(IntTest)

    def mid_rapidity_charge(self, Ypred, Ytest):
        etami, etaMi = np.abs(self.EtaOut + 0.5).argmin(), np.abs(self.EtaOut - 0.5).argmin()
        IntPred = self.ComputeIntegralArray(Ypred[etami:etaMi])
        IntTest = self.ComputeIntegralArray(Ytest[etami:etaMi])
        return np.array(IntPred) - np.array(IntTest)

    def mean_absolute_error(self, Ypred, Ytest):
        Ymean = np.mean(Ytest, axis=1)
        return np.mean(np.abs(Ypred - Ytest), axis=1)/Ymean * 100

    def root_mean_squared_error(self, Ypred, Ytest):
        Ymean = np.mean(Ytest, axis=1)
        mse = np.mean((Ypred - Ytest) ** 2, axis=1)
        return np.sqrt(mse)/Ymean * 100

    def r_squared(self, Ypred, Ytest):
        y_mean = np.mean(Ytest, axis=1, keepdims=True)
        ss_total = np.sum((Ytest - y_mean) ** 2, axis=1)
        ss_residual = np.sum((Ytest - Ypred) ** 2, axis=1)
        return 1 - (ss_residual / ss_total)

    def correlation_coefficient(self, Ypred, Ytest):
        means_test = np.mean(Ytest, axis=1, keepdims=True)
        means_pred = np.mean(Ypred, axis=1, keepdims=True)
        numerators = np.sum((Ytest - means_test) * (Ypred - means_pred), axis=1)
        denominators = np.sqrt(np.sum((Ytest - means_test) ** 2, axis=1) *
                               np.sum((Ypred - means_pred) ** 2, axis=1))
        return numerators / denominators

    def ComputeMAE(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.mean_absolute_error(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def ComputeRMSE(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.root_mean_squared_error(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def ComputeR2(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.r_squared(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def ComputeCorrelation(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.correlation_coefficient(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def ComputeGlobalCharge(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.global_charge(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def ComputeMidCharge(self, Xtest, Ytest, Ypred, CTest):
        IndexDict = self.GetCentralityIndices(CTest)
        return {centr:self.mid_rapidity_charge(Ypred[indexes], Ytest[indexes]) for centr, indexes in IndexDict.items()}

    def GetRaw(self, Xtest, Ytest, Ypred, CTest):
        return {"Eta":self.EtaOut, "Xtest":Xtest, "Ytest":Ytest, "Ypred":Ypred, "Centralities":CTest}


    def Full(self, Xtest, Ytest, Ypred, CTest):
        return {"MAE":self.ComputeMAE(Xtest, Ytest, Ypred, CTest), 
                "RMSE":self.ComputeRMSE(Xtest, Ytest, Ypred, CTest), 
                "R2":self.ComputeR2(Xtest, Ytest, Ypred, CTest), 
                "Corr":self.ComputeCorrelation(Xtest, Ytest, Ypred, CTest), 
                "GC":self.ComputeGlobalCharge(Xtest, Ytest, Ypred, CTest),
                "MidRap":self.ComputeMidCharge(Xtest, Ytest, Ypred, CTest)
                }

    def Raw(self, Xtest, Ytest, Ypred, CTest):
        return {"GetRaw":self.GetRaw(Xtest, Ytest, Ypred, CTest)}


