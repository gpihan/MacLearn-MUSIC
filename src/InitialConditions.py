from src.initial_conditions.Init3DMCG import Init3DMCG
import numpy as np

class InitialConditions():
    def __init__(self, Parameters):
        Param = Parameters.fromGeneralParameters
        InitCondParam = Parameters.fromInitialConditions
        if Param["InitialConditions"] == "3DMCGlauber":
            self.InitialCondition = Init3DMCG(Param, InitCondParam, Parameters.InitPath)
        self.parameters = InitCondParam
        self.PredictionOn = Param["PredictionOn"]
        self.ForCurrentCharge = []
        self.possibleNuclei = Param["PossibleNuclei"]
        self.NucEncoder = {a:i for i,a in enumerate(self.possibleNuclei)} 

        # Add initial conditions if new initial conditions codes are available
        # Also add in the .gitmodules

    def getFeatures(self):
        self.features = [self.NucEncoder[self.parameters["Projectile"]], self.parameters["roots"]]

    def SelectFeatures(self, ModelsFeaturesType, ModelsPossibleFeatures):
        self.FeaturesToAdd = []
        for i, (ModelFeatureType, PossFeatures) in enumerate(zip(ModelsFeaturesType, ModelsPossibleFeatures)):
            if ModelFeatureType == 0:
                self.FeaturesToAdd.append([None])
            elif ModelFeatureType == 1:
                if any([self.features[0] == possibility for possibility in PossFeatures]):
                    self.FeaturesToAdd.append([self.features[0]])
                else:
                    print("Warning: Collisions system for prediction and training Nucleus are different.")
                    print("Nucleus feature set on one of the possible nucleus in trained model.")
                    self.FeaturesToAdd.append([PossFeatures[0]])
            elif ModelFeatureType == 2:
                if any([self.features[1] == possibility for possibility in PossFeatures]):
                    self.FeaturesToAdd.append([self.features[1]])
                else:
                    print("Warning: sqrt(s) for prediction and training are different.")
                    print("Energy feature set on one of the possible in trained model.")
                    self.FeaturesToAdd.append([PossFeatures[-1]])
            elif ModelFeatureType == 3:
                checkNuc = any([self.features[0] == possibility for possibility in PossFeatures])
                checkEn = any([self.features[1] == possibility for possibility in PossFeatures])
                if checkNuc and checkEn:
                    self.FeaturesToAdd.append(self.features)
                elif checkEn:
                    print("Warning: Collisions system for prediction and training Nucleus are different.")
                    print("Nucleus feature set on one of the possible nucleus in trained model.")
                    self.FeaturesToAdd.append([PossFeatures[0], self.features[1]])
                elif checkNuc:
                    print("Warning: sqrt(s) for prediction and training are different.")
                    print("Energy feature set on one of the possible in trained model.")
                    self.FeaturesToAdd.append([self.features[0], PossFeatures[-1]])
                else:
                    print("Warning: Collisions system for prediction and training Nucleus are different.")
                    print("Nucleus feature set on one of the possible nucleus in trained model.")
                    print("Warning: sqrt(s) for prediction and training are different.")
                    print("Energy feature set on one of the possible in trained model.")
                    self.FeaturesToAdd.append([PossFeatures[0], PossFeatures[-1]])

    def AddFeatures(self, i):
        if self.FeaturesToAdd[i][0] == None:
            pass
        elif len(self.FeaturesToAdd[i])==1:
            for key in ["ed", "nb", "nq"]:
                self.InitArrayDict[key] = np.hstack((self.InitArrayDict[key], np.full((self.InitArrayDict[key].shape[0], 1), self.FeaturesToAdd[i][0])))
        elif len(self.FeaturesToAdd[i])==2:
            for key in ["ed", "nb", "nq"]:
                arrTemp = np.hstack((self.InitArrayDict[key], np.full((self.InitArrayDict[key].shape[0], 1), self.FeaturesToAdd[i][0])))
                self.InitArrayDict[key] = np.hstack((arrTemp, np.full((arrTemp.shape[0], 1), self.FeaturesToAdd[i][1])))
            
    def CleanFeatures(self):
        for key in ["ed", "nb", "nq"]:
            self.InitArrayDict[key] = self.InitArrayDict[key][:,:self.OrigLen]

    def generate(self):
        names = ["eta", "ed", "nb", "nq"]
        self.InitArrayDict = {name:stuff for name, stuff in zip(names, tuple(self.InitialCondition.generate()))}
        self.OrigLen = len(self.InitArrayDict["nb"][0,:])

    def get(self, charge):
        if charge == "B":
            key = "nb"
        elif charge == "Q":
            key = "nq"
        self.ForCurrentCharge = self.InitArrayDict[key]
