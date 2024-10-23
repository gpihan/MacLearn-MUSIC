# This class contains all analysis functions
# 1) Analysis for training models performance.
# 2) Analysis on the predicted curves.
import numpy as np


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
            print(self.D.keys())
            print(self.AnalysisOnTrain)
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
            Ypred = model.predictOntest(Xtest)
            Xtest = np.array(Xtest)
            Ytest = np.array(Ytest)
            Ypred = np.array(Ypred)
            for func in self.TrainFunc:
                self.TrainTestDict[func] = self.D[func](self, Xtest, Ytest, Ypred)
        else:
            self.TrainTestDict = {}


    "ComputeRMSDiff", "MidRapidityDiff", "MidRapidityVar"
    def ComputeRMSDiff(self, Xtest, Ytest, Ypred):
        return np.sqrt(np.sum((Ytest - Ypred)**2, axis=0)/len(Ytest[:,0])) 

    def MidRapidityDiff(self, Xtest, Ytest, Ypred):
        y1, y2 = -0.5, 0.5
        i1 = np.argmin(np.abs(self.EtaOut - y1))
        i2 = np.argmin(np.abs(self.EtaOut - y2))
        Ymid = Ytest[:,i1:i2]
        YmidPred = Ypred[:,i1:i2]
        Diff = Ymid - YmidPred
        return Diff

        






