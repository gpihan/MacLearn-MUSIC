import sys
import importlib

class Parameters:
    def __init__(self):
        self.dict = {}

    def read_parameters(self, path, paramType):
        try:
           spec = importlib.util.spec_from_file_location(paramType, path)
           module = importlib.util.module_from_spec(spec)
           sys.modules[paramType] = module
           spec.loader.exec_module(module)
           exec("self.dict = module."+paramType)
        except FileNotFoundError:
            print(f"File '{path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
