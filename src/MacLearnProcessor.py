# This class manage all the processes to connect models with initial conditions
# train the model and make the predictions



class MacLearnProcessor():
    
    def __init__(self, Parameters):
        self.QueryModels = Parameters.fromGeneralParameters["model_names"]
        self.QueryModelType = Parameters.fromGeneralParameters["prediction_types"]
        self.QueryTrainedOn = Parameters.fromGeneralParameters["TrainedOn"]
        self.TrainedModels = []
        self.TrainedModelPath = "TrainedModels"
    
    def LoadModelTags():
        # Load the model tags for checking 
        # Dictionary?? (That then should be inside the trained models)
        pass 
    
    def CheckTrainedModels():
        # Check which input model is not in the trainedModel
        pass 

    def GenerateInitialConditions(self):
        pass

    def GenerateTrainingData(self):
        pass
    
    def TrainModels(self):
        # only the models that needs to be trained
        # = the ones whos tag is not equal 
        # to the tag of one trained models 
        pass

    def LoadModels(self, forRunMode=0):
        # If run mode = 0: load models that are not in the TrainedModel.
        # If run mode = 1: load the models that are in the TrainedModel
        pass 

    def GeneratePredictions(self):
        pass

    def Generate_object(self):
        pass