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

    








