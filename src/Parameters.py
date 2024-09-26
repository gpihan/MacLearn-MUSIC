import sys
import importlib
from .utils import *

class Parameters:
    def __init__(self):
        self.fromGeneralParameters = {}
        self.fromInitialConditions = {}
        self.Nev = 0
        self.ParamPath = ""
        self.InitPath = ""
    
    def ReadUserInput(self):
        try:
            self.Nev = int(sys.argv[1])
            self.ParamPath = str(sys.argv[2])
            self.InitPath = str(sys.argv[3])
        except IndexError:
            PrintHelp()
            exit(0)

    def read_parameters_for(self, paramType, DictName=""):
        if paramType == "InitialConditions":
            path = self.InitPath
        elif paramType == "GeneralParameters":
            path = self.ParamPath
        else:
            print("Parameters type can be InitialConditions or GeneralParameters")
            sys.exit()
        try:
           spec = importlib.util.spec_from_file_location(DictName, path)
           module = importlib.util.module_from_spec(spec)
           sys.modules[paramType] = module
           spec.loader.exec_module(module)
           exec("self.from"+paramType+" = module."+DictName)
        except FileNotFoundError:
            print(f"File '{path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
