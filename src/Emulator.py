# This class is used as a wrapper class for trained model
# Once a model is trained and place in the TrainedModels dir
# this class reads it, load it and wrap it up in a pickle object 
# ready for prediction

import pickle
import sys

class Emulator:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model_path = "TrainedModels/"+model_name
        
    def load_emulator(self):
        try:
            with open(self.model_path, "rb") as pf:
                model_dict = pickle.load(pf)
        except FileNotFoundError:
            print("The required model is not in the TrainedModels directory")
            sys.exit()
        
        # To adapt to the saved trained model dict
        self.model = model_dict["model"]
        self.model_metadata = model_dict["metadata"]


        # To determine
        self.model.load()

    def predict(self, initial_inputs):
        return self.model.predict(initial_inputs)