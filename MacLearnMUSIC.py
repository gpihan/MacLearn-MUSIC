from src.utils import *
from src.Parameters import Parameters
import sys

if __name__ == "__main__":
    
    # Parse user input
    try:
        nev, path_to_parameters_file, path_to_3dMCGlauber_parameters = int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
    except IndexError:
        printHelp()
        exit(0)

    # Read parameters from parameter file
    # The second string argument is the name of the subdictionary
    # inside the parameter_.py file
    ParamModels = Parameters()
    ParamModels.read_parameters(path_to_parameters_file, "general_parameters")

    Param3dMCG = Parameters()
    Param3dMCG.read_parameters(path_to_3dMCGlauber_parameters, "para_dict")

    ParamTrData = Parameters()
    ParamTrData.read_parameters(path_to_parameters_file, "data_parameters")

    
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

    # Adapt the code for computation on the cluster 
    # parallelize each predictions as much as possible
    # parallelize centralities (or modelType BB, Bp, QQ ...) 
    # with joblib or concurrent.futures
    








