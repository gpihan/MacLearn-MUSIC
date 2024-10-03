# This class handles all display and prints


class Display():

    def __init__(self):
        self.verbose = True
        
        
    def getVerbosity(self, param):
        self.verbose = param.fromGeneralParameters["verbose"]

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
            print("!:#MacLearn MUSIC#:! Let this machine play some MUSIC")
            
    def Message(self, string):
        if self.verbose:
            print(string)

