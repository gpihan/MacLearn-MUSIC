from src.utils import *
from src.Parameters import Parameters
from src.MacLearnProcessor import MacLearnProcessor
from src.Display import Display
import sys

if __name__ == "__main__":
    
    Display = Display()

    # Read parameters from parameter file
    Parameters = Parameters()
    Parameters.ReadUserInput()
    Parameters.read_parameters_for("GeneralParameters", "parameters")
    Parameters.read_parameters_for("InitialConditions", "para_dict")

    Display.getVerbosity(Parameters)
    Display.Title()

    #print(Parameters.fromGeneralParameters["model_names"])
    
    # Give Parameters.fromGeneralParameters or Parameters.fromInitialConditions 
    # Class must have dictionaries

    if Parameters.fromGeneralParameters["mode"] == 0:
        Display.Message("Mode set to: training models only")
    elif Parameters.fromGeneralParameters["mode"] == 1:
        Display.Message("Mode set to: predictions only")
    elif Parameters.fromGeneralParameters["mode"] == 2:
        Display.Message("Mode set to: training models and predictions")
    elif Parameters.fromGeneralParameters["mode"] == 3:
        Display.Message("Mode set to: models Analysis only")
    elif Parameters.fromGeneralParameters["mode"] == 4:
        Display.Message("Mode set to: training and analysis only")
    else:
        Display.ModeHelper()
        sys.exit()

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