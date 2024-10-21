import sys
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
import pickle
from ..Data import Data



class RidgeRegressor():
    def __init__(self, Param):
        self.pipeline = make_pipeline(
            PolynomialFeatures(degree=Param["PolyDegree"]),
            Ridge(alpha=Param["RidgeAlpha"])
        )
        #self.fname = Param["Output_file_name"]
        self.fname = "TestRidgeRegressor.dat"

    def train(self, TrainingData, chargeIn, chargeOut):
        if TrainingData.IsProperlyShaped:
            Xtrain, Ytrain = tuple(TrainingData.SplitTrainedData[chargeIn][chargeOut]["Train"])
            self.pipeline.fit(Xtrain, Ytrain)
            
            #Nfeatures = TrainingData.NumberOfFeatures
            #Xtest, Ytest = tuple(TrainingData.SplitTrainedData[chargeIn][chargeOut]["Test"])
            #Ypred = self.pipeline.predict(Xtest)
            #N = 24
            #plt.plot(np.linspace(-1,1, len(Ypred[N][:-Nfeatures])), Ypred[N][:-Nfeatures], label="prediction")
            #plt.plot(np.linspace(-1,1, len(Ytest[N][:-Nfeatures])), Ytest[N][:-Nfeatures], label="Truth")
            #plt.plot(np.linspace(-1,1, len(Xtest[N][:-Nfeatures])), Xtest[N][:-Nfeatures], label="Initial")
            #plt.xlabel("y")
            #plt.ylabel("$d\\mathrm{N}_B/dy$")
            #plt.legend()
            #plt.show()
        else:
            print("Error: Training data is not shaped properly")
            sys.exit()

    def predict(self, Y):
        return self.pipeline.predict(Y)

    def save(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self, f)


