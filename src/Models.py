# This class is an interface for the model training in src/models. 
# It trains the input model and save it as a trained model 
# in the TrainedModels directory in a pickle dumped python dictionary.
# The dictionary also contains the training metadata (initial and final type, nucleus)
# The model metadata (all numbers involved in the models)
# The initial conditions used to perform the training metadata (for instance 3dMCGlauber input dictionary)

import pickle

from src.models.Transformer import *
from src.models.RidgeRegression import RidgeRegressor
from src.Data import Data


class Model:
    def __init__(self, model_type, Param):
        self.parameters = Param
        self.model_type = model_type
        if model_type == 'Transformer':
            self.model = Transformer(Param)
        elif model_type == 'RidgeRegressor':
            self.model = RidgeRegressor(Param)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, TrainingData, chargeIn, chargeOut):
        self.model.train(TrainingData, chargeIn, chargeOut)
        self.make_metadata(TrainingData, chargeIn, chargeOut)
        self.trained_flag = True

    def make_metadata(self, TrainingData, chargeIn, chargeOut):
        self.metadata = {"ModelParameters":self.parameters, 
                         "NumberOfFeaturesFeatures":TrainingData.NumberOfFeatures,
                         "FeaturesType":TrainingData.FeatureType,
                         "PossibleFeatures":TrainingData.PossibleFeatures,
                         "ChargeIn":chargeIn,
                         "ChargeOut":chargeOut,
                         "Type":self.model_type,
                         "PathToTrainingData":TrainingData.DataPath
                         }

    def save(self):
        if self.trained_flag:
            # Transformer_Au_Bp.pkl for instance
            dirname = self.metadata["PathToTrainingData"].split("/")[-1]
            fname = self.model_type+dirname+"_"+self.metadata["ChargeIn"]+self.metadata["ChargeOut"]+".pkl"
            Dct = {"model":self.model}
            Dct = {**self.metadata, **Dct}
            fi = open("TrainedModels/"+fname, 'wb')
            pickle.dump(Dct, fi)
            fi.close()

            # Make sure that Emulator reads it the same way
