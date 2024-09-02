from abc import ABC, abstractmethod
import pickle



class Model(ABC):
    @abstractmethod
    def __init__(self, Param):
        pass

    @abstractmethod
    def train(self,  X_train, Y_train, X_test, Y_test):
        pass

    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def predict(self, Y):
        pass

    @abstracmethod
    def save(self):
        pass

    @classmethod
    def load_trained_model(cls, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
