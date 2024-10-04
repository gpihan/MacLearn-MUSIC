# This class is used as a wrapper class for trained model
# Once a model is trained and place in the TrainedModels dir
# this class reads it, load it and wrap it up in a pickle object 
# ready for prediction

import pickle
import sys
from .InitialConditions import InitialConditions

class Emulator:
    def __init__(self, Param):
        self.ModelNames = Param["ModelNames"]
        self.ModelsPath = ["TrainedModels/"+modelName for modelName in Param["ModelNames"]]
        self.EmulatorLoaded = False
        self.PredictionOn = Param["PredictionOn"]
        self.OutputFolder = "OUTPUT/"+Param["OutputFolder"]

    def loadModels(self):
        self.Models = []
        for modelPath in self.ModelsPath:
            try:
                with open(modelPath, "rb") as pf:
                    self.Models.append(pickle.load(pf))
            except FileNotFoundError:
                print("The required model is not in the TrainedModels directory")
                sys.exit()
        self.EmulatorLoaded = True

    def ReadModelsFeatures(self):
        self.ModelsFeaturesType = [Model["FeaturesType"] for Model in self.Models]
        self.ModelsPossibleFeatures = [Model["PossibleFeatures"] for Model in self.Models]

    def CheckModelsMetaData(self, modelDict):
        for parameter, value in modelDict.items():
            if parameter == "model" or parameter == "ModelParameters":
                continue
            else:
                print(parameter, ":", value)

    def predict(self, InitialConditions):
        for i, (Model, charge, modelname) in enumerate(zip(self.Models, self.PredictionOn, self.ModelNames)):
            InitialConditions.AddFeatures(i)
            InitialConditions.get(charge)
            Model["model"].predict(InitialConditions.ForCurrentCharge)
            if InitialConditions.PredictionMode == 0:
                Outpath = InitialConditions.InitialCondition.Folder_path
                InputF = ""
            elif InitialConditions.PredictionMode == 1:
                Outpath = InitialConditions.PredictOutputPath
                InputF = InitialConditions.InitFolderPath
            Model["model"].save_predictions(Outpath, charge, modelname, InputFolderName=InputF)
            InitialConditions.CleanFeatures()