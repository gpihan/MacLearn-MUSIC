from Model import Model
from sklearn.pipeline import make_pipeline
import numpy as np


class RidgeRegressor(Model):
    def __init__(self, Param):
        self.pipeline = make_pipeline(
            PolynomialFeatures(degree=Param["Polydegree"]),
            Ridge(alpha=Param["RidgeAlpha"])
        )
        self.fname = Param["Output_file_name"]

    def train(self,  X_train, Y_train, X_test, Y_test):
        self.pipeline.fit(X_train, Y_train)

    def predict(self, Y):
        return self.pipeline.predict(Y)

    def save(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self, f)


