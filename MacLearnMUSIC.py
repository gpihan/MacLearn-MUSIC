from src.utils import *
from src.Parameters import Parameters
from src.MacLearnProcessor import MacLearnProcessor
from src.Display import Display
from src.Emulator import Emulator
from src.models.RidgeRegression import RidgeRegressor
from src.Data import Data
from src.Models import Model
from src.InitialConditions import InitialConditions
import numpy as np
import sys

if __name__ == "__main__":
    
    Display = Display()

    # Read parameters from parameter file
    Parameters = Parameters()
    Parameters.ReadUserInput()
    Parameters.read_parameters_for("GeneralParameters", "parameters")
    Parameters.read_parameters_for("InitialConditions", "para_dict")
    

    ######### Training 
    #TrainingData = Data(Parameters.fromGeneralParameters)
    #TrainingData.load_data()
    #TrainingData.PrepareTrainingData()
    #TrainingData.PerformSplitGaussianSmoothing()
    #print(np.array(TrainingData.SplitTrainedData["B"]["NetNeutron"]["Train"][0]).shape)


    #Ridgemodel = Model("RidgeRegressor", Parameters.fromGeneralParameters)
    #Transformermodel = Model("Transformer", Parameters.fromGeneralParameters)
    #Ridgemodel.train(TrainingData, "B", "B")
    #Ridgemodel.save()
    #Transformermodel.train(TrainingData, "B", "NetProton")
    #Transformermodel.save()
    


    ###### Predictions
    ModelEmulator = Emulator(Parameters.fromGeneralParameters)

    ModelEmulator.loadModels()
    ModelEmulator.ReadModelsFeatures()
    
    InitialCondition = InitialConditions(Parameters)
    InitialCondition.getFeatures()
    InitialCondition.SelectFeatures(ModelEmulator.ModelsFeaturesType, 
                                    ModelEmulator.ModelsPossibleFeatures)
    InitialCondition.generate()
    ModelEmulator.predict(InitialCondition)



    #Display.getVerbosity(Parameters)
    #Display.Title()

    #MacLearnProcessor = MacLearnProcessor(Parameters)
    ##print(Parameters.fromGeneralParameters["model_names"])

    #if Parameters.fromGeneralParameters["mode"] == 0:
    #    Display.Message("Mode set to: training models only")
    #    Display.Message("Proceeding to training")
    #    Display.Message("Model query: "+Parameters.fromGeneralParameters["model_names"].join(" "))
    #    Display.Message("Train on data in ", Parameters.fromGeneralParameters["Data_path"])

    #    MacLearnProcessor.LoadModelTags()
    #    MacLearnProcessor.CheckTrainedModels(for_mode=0)
    #    MacLearnProcessor.GenerateTrainingData()
    #    MacLearnProcessor.LoadModels(forRunMode=0)
    #    MacLearnProcessor.TrainModels()
    #    MacLearnProcessor.Generate_object()
    #    
    #    Display.Message("Model trained")
    #    Display.Message("Saved as pickle objects in TrainedModels/")

    #elif Parameters.fromGeneralParameters["mode"] == 1:
    #    Display.Message("Mode set to: predictions only")
    #    Display.Message("Proceeding to predictions using models "+Parameters.fromGeneralParameters["model_names"].join(" "))
    #    Display.Message("Initial conditions query: "+ Parameters.fromGeneralParameters["InitialConditions"])
    #    Display.Message("Number of events", Parameters.Nev)
    #    Display.Message("Type query: ", Parameters.fromGeneralParameters["prediction_types"])
    #    
    #    MacLearnProcessor.LoadModelTags()
    #    MacLearnProcessor.CheckTrainedModels()
    #    MacLearnProcessor.GenerateInitialConditions()
    #    MacLearnProcessor.LoadModels(forRunMode=1)
    #    MacLearnProcessor.GeneratePredictions()
    #    
    #    Display.Message("Predictions done")
    #    Display.Message("Saved as pickle dictionary in ")
    #    # Check output folder treatment properly


    #elif Parameters.fromGeneralParameters["mode"] == 2:
    #    Display.Message("Mode set to: training models and predictions")
    #elif Parameters.fromGeneralParameters["mode"] == 3:
    #    Display.Message("Mode set to: models Analysis only")
    #elif Parameters.fromGeneralParameters["mode"] == 4:
    #    Display.Message("Mode set to: training and analysis only")
    #else:
    #    Display.ModeHelper()
    #    sys.exit()

    #print(Parameters.fromInitialConditions["Projectile"])
    
    #MLP = MacLearnProcessor(Parameters)
    #MLP.CheckTrainedModels()

    
    # Instantiate MacLearnProcessor
    # Check if models need to be trained 
    # if so, read the training data, (check formatting of the data) train the models
    # save the trained models in TrainedModels
    # Compute the initial conditions from initialConditions object
    # use sym link to compute these directly into the output folder
    # generate an emulator object for each trained model asked
    # move emulator object as well as a copy of emulator class 
    # in the output folder
    # perform the prediction using the MLDriver in 3dMCGlauber
    # (re adapt the code)
    # ask why the shape of the input data does not use encoder anymore
    # save the prediction into the same folder 
    # profit

    # write the analysis on the trained models and predictions

    
    # Adapt the code for computation on the cluster 
    # parallelize each predictions as much as possible
    # parallelize centralities (or modelType BB, Bp, QQ ...) 
    # with joblib or concurrent.futures