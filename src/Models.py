# This class is an interface for the model training in src/models. 
# It trains the input model and save it as a trained model 
# in the TrainedModels directory in a pickle dumped python dictionary.
# The dictionary also contains the training metadata (initial and final type, nucleus)
# The model metadata (all numbers involved in the models)
# The initial conditions used to perform the training metadata (for instance 3dMCGlauber input dictionary)

import pickle

from src.models.Transformer import *
from src.models.RidgeRegression import RidgeRegressor


class Model:
    def __init__(self, model_type, Param, InitCondParam):
        self.parameters = Param
        self.InitCondParam = InitCondParam
        self.model_type = model_type
        if model_type == 'Transformer':
            self.model = Transformer(Param)
        elif model_type == 'RidgeRegression':
            self.model = RidgeRegressor(Param)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, Xtrain, Ytrain, Xtest, Ytest, training_metadata):
        self.model.train(Xtrain, Ytrain, Xtest, Ytest)
        self.training_metadata = training_metadata
        self.trained_flag = True

    def make_metadata(self):
        self.metadata = {"ModelParameters":self.parameters, 
                         "InitialConditionsParameters":self.InitCondParam,
                         "training_parameters":self.training_metadata}

    def save(self):
        if self.trained_flag:
            # Transformer_Au_Bp.pkl for instance
            fname = self.model_type+"_"+self.training_metadata["Nucleus"]+"_"+self.training_metadata["TrainType"]+".pkl"
            Dct = {"model":self.model}
            Dct = {**self.metadata, **Dct}
            fi = open("TrainedModels/"+fname, 'wb')
            pickle.dump(Dct, fi)
            fi.close()

            # Make sure that Emulator reads it the same way
