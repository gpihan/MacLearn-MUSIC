import numpy as np
import matplotlib.pyplot as plt
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
    

    # Read parameters from parameter file
    Parameters = Parameters()
    Parameters.ReadUserInput()
    Parameters.read_parameters_for("GeneralParameters", "parameters")
    Parameters.read_parameters_for("InitialConditions", "para_dict")
    
    Display = Display(Parameters.fromGeneralParameters)
    Display.Title()
    checkLibraries(Display)
    Display.BlankSpace()

    Display.StartMessage()

    if Parameters.fromGeneralParameters["RunningMode"] == 0:
        ######### Training Mode

        Display.Message("Running on Training mode")
        Display.Message("Loading Training Data in "+Parameters.fromGeneralParameters["DataPath"])
        # Reading and structuring data
        TrainingData = Data(Parameters.fromGeneralParameters)
        TrainingData.load_data()
        Display.Message("Reshaping Training Data.")
        TrainingData.PrepareTrainingData()
        Display.Message("Smooth Training Data with Gaussian Kernel")
        TrainingData.PerformSplitGaussianSmoothing()

        # Read input and output charge queries.
        InputCharge = Parameters.fromGeneralParameters["InputCharge"]
        OutputCharge = Parameters.fromGeneralParameters["OutputCharge"]

        # Prepare Analysis 

        Display.Message("Prepare Training Analysis")
        Analysis = Analyser(Parameters.fromGeneralParameters)
        Analysis.loadAnalysis(Analyser.__dict__)

        Display.Message("Train models.")
        # Perform the training on data 
        for ModelType in Parameters.fromGeneralParameters["ModelTypes"]:
            Display.Message("\t"+ModelType+":")
            model = Model(ModelType, Parameters.fromGeneralParameters)
            Display.Message("\t\tTrain")
            model.train(TrainingData, InputCharge, OutputCharge)
            Display.Message("\t\tPerform Aanalysis")
            Analysis.PerformAnalysis(model, TrainingData, Analyser.__dict__)
            Display.Message("\t\tSave")
            model.save(Analysis.TrainTestDict)
            Display.Message("\tDone")

        Display.EndMessage()

    elif Parameters.fromGeneralParameters["RunningMode"] == 1:
        ######### Prediction mode

        Display.Message("Running on Prediction mode")
        ModelEmulator = Emulator(Parameters.fromGeneralParameters)
        Display.Message("Load trained models")
        ModelEmulator.loadModels()
        Display.Message("Read models features")
        ModelEmulator.ReadModelsFeatures()
    
        Display.Message("Prepare Ininitial conditions")
        InitialCondition = InitialConditions(Parameters)
        if Parameters.fromGeneralParameters["PredictionMode"] == 0:
            # Generating initial conditions 
            Display.Message("Prediction on generating mode.")
            Display.Message("Select relevant classification features.")
            InitialCondition.getFeatures()
            InitialCondition.SelectFeatures(ModelEmulator.ModelsFeaturesType, 
                                       ModelEmulator.ModelsPossibleFeatures)
            Display.Message("Generate initial conditions.")
            InitialCondition.generate()
        elif Parameters.fromGeneralParameters["PredictionMode"] == 1:
            # read initial conditions 
            Display.Message("Prediction on read mode.")
            Display.Message("Select relevant classification features.")
            InitialCondition.readFeatures()
            InitialCondition.SelectFeatures(ModelEmulator.ModelsFeaturesType, 
                                       ModelEmulator.ModelsPossibleFeatures)
            Display.Message("Read existing initial conditions.")
            InitialCondition.read()
        
        # Perform the prediction
        Display.Message("Perform predicitons on initial conditions.")
        ModelEmulator.predict(InitialCondition)
        Display.EndMessage()
    
    elif Parameters.fromGeneralParameters["RunningMode"] == 2:
        ModelEmulator = Emulator(Parameters.fromGeneralParameters)
        ModelEmulator.loadModels()
        ModelEmulator.ReadModelsFeatures()


        #Yt, sigt, Yp, sigYp = ModelEmulator.Models[0]["MidRapidityDiff"]

        #plt.scatter(np.linspace(0,1,len(Yp)), np.abs(Yp-np.mean(Yp))**2/sigt**2)
        #plt.show()


        DAT = ModelEmulator.Models[0]["Full"]
        print(DAT["ComputeRMSDiffCentrality"]["0-10"])
        #Yt, Yp = DAT[0], DAT[1]
        #i = 2180
        #plt.plot(np.linspace(0,1,len(Yt[i,:])), Yt[i,:], label="Truth")
        #plt.plot(np.linspace(0,1,len(Yp[i,:])), Yp[i,:], label="prediction")
        ##sigmaY = np.std(Y)
        ##plt.scatter(np.linspace(0,1,len(Y)), Y/sigmaY)
        #plt.show()



    
    # Adapt the code for computation on the cluster 
    # parallelize each predictions as much as possible
    # parallelize centralities (or modelType BB, Bp, QQ ...) 
    # with joblib or concurrent.futures
