import numpy as np
import sys
sys.path.append('path_to_src_directory')
from src.utils import *
from src.Parameters import Parameters
from src.Display import Display
from src.Emulator import Emulator
from src.models.RidgeRegression import RidgeRegressor
from src.Data import Data
from src.Models import Model
from src.InitialConditions import InitialConditions
from src.Analyser import Analyser

if __name__ == "__main__":
    
    #checkLibraries()
    Display = Display()

    # Read parameters from parameter file
    Parameters = Parameters()
    Parameters.ReadUserInput()
    Parameters.read_parameters_for("GeneralParameters", "parameters")
    Parameters.read_parameters_for("InitialConditions", "para_dict")
    
    if Parameters.fromGeneralParameters["RunningMode"] == 0:
        ######### Training Mode

        # Reading and structuring data
        TrainingData = Data(Parameters.fromGeneralParameters)
        TrainingData.load_data()
        TrainingData.PrepareTrainingData()
        TrainingData.PerformSplitGaussianSmoothing()

        # Read input and output charge queries.
        InputCharge = Parameters.fromGeneralParameters["InputCharge"]
        OutputCharge = Parameters.fromGeneralParameters["OutputCharge"]

        # Prepare Analysis 

        Analysis = Analyser(Parameters.fromGeneralParameters)
        Analysis.loadAnalysis(Analyser.__dict__)

        
        # Perform the training on data 
        for ModelType in Parameters.fromGeneralParameters["ModelTypes"]:
            model = Model(ModelType, Parameters.fromGeneralParameters)
            model.train(TrainingData, InputCharge, OutputCharge)
            Analysis.PerformAnalysis(model, TrainingData, Analyser.__dict__)
            model.save(Analysis.TrainTestDict)

    elif Parameters.fromGeneralParameters["RunningMode"] == 1:
        ######### Prediction mode

        ModelEmulator = Emulator(Parameters.fromGeneralParameters)
        ModelEmulator.loadModels()
        ModelEmulator.ReadModelsFeatures()
    
        InitialCondition = InitialConditions(Parameters)
        if Parameters.fromGeneralParameters["PredictionMode"] == 0:
            # Generating initial conditions 
            InitialCondition.getFeatures()
            InitialCondition.SelectFeatures(ModelEmulator.ModelsFeaturesType, 
                                       ModelEmulator.ModelsPossibleFeatures)
            InitialCondition.generate()
        elif Parameters.fromGeneralParameters["PredictionMode"] == 1:
            # read initial conditions 
            InitialCondition.readFeatures()
            InitialCondition.SelectFeatures(ModelEmulator.ModelsFeaturesType, 
                                       ModelEmulator.ModelsPossibleFeatures)
            InitialCondition.read()
        
        # Perform the prediction
        ModelEmulator.predict(InitialCondition)
    
    elif Parameters.fromGeneralParameters["RunningMode"] == 2:
        ModelEmulator = Emulator(Parameters.fromGeneralParameters)
        ModelEmulator.loadModels()
        ModelEmulator.ReadModelsFeatures()
        print(ModelEmulator.Models[0]["MidRapidityDiff"])


    
    # Adapt the code for computation on the cluster 
    # parallelize each predictions as much as possible
    # parallelize centralities (or modelType BB, Bp, QQ ...) 
    # with joblib or concurrent.futures
