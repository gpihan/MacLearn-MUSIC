# This class handles all display and prints
import time
import numpy as np

class Display():

    def __init__(self, Param):
        self.verbose = Param["verbose"]
        self.initTime = time.time()
        
        
    def Helper(self):
        print("Usage: python3 MacLearnMUSIC.py nev path_to_parameters path_to_3dMCGlauber_parameters")
        print("path_to_parameters: The parameter dictionnary for prediction models")
        print("path_to_3dMCGlauber_parameters: The parameter dictionnary for 3DMCGlauber")
    
    def ModeHelper(self):
        print("Possible modes:")
        print("mode 0: Training only")
        print("mode 1: Predictions only")
        print("mode 2: Training and predictions")
        print("mode 3: Analysis only")
        print("mode 4: Training and analysis")
    
    def Title(self):
        if self.verbose:
    
            print(" "*20+"-"*60+" "*20)
            print()                
            print("MacLearn MUSIC v1.0".center(100, ' '))
            print()
            print("Machine Learning interface for iEBE-MUSIC simulations.".center(100, ' '))
            print("github: https://github.com/gpihan/MacLearn-MUSIC".center(100, ' '))
            print("Gregoire Pihan - 2024".center(100, ' '))
            print()
            print(" "*20+"-"*60+" "*20)
            
    def Message(self, string):
        if self.verbose:
            print("["+time.strftime("%H:%M:%S", time.localtime())+"]", string)

    def StartMessage(self):
        if self.verbose:
            print(" "*20+"-"*60+" "*20)
            print("Start".center(100, ' '))
            print(" "*20+"-"*60+" "*20)
            print()


    def EndMessage(self):
        if self.verbose:
            print()
            print(" "*20+"-"*60+" "*20)
            print("End".center(100, ' '))
            print(" "*20+"-"*60+" "*20)
            print()
            print("Estimated total running time: ", round(time.time() - self.initTime, 1), "seconds")
            print()
            print("Thanks for using MacLearn-MUSIC!")

    def BlankSpace(self):
        if self.verbose:
            print()
