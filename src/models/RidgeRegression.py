import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
import pickle



class RidgeRegressor():
    def __init__(self, TrainingData, degree, alpha):
        self.pipeline = make_pipeline(
            PolynomialFeatures(degree=degree),
            Ridge(alpha=alpha)
        )
        #self.fname = Param["Output_file_name"]
        self.fname = "TestRidgeRegressor.dat"

    # TO DO: define the function as in aryans code
    def finetune():
        pass

    def train(self,  X_train, Y_train):
        self.pipeline.fit(X_train, Y_train)

    def predict(self, Y):
        return self.pipeline.predict(Y)

    def save(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self, f)


