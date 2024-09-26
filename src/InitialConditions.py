from src.initial_conditions.Init3DMCG import Init3DMCG

class InitialConditions():
    def __init__(self, Parameters, InitialConditionsParameters):
        if Parameters["InitialConditions"] == "3DMCG":
            self.InitialCondition = Init3DMCG()
            self.parameters = InitialConditionsParameters
        # Add initial conditions if new initial conditions codes are available
        # Also add in the .gitmodules
        
    # Consider the features in the dataset: Training for 200 GeV Ru? have features 200 1 associated.

    def generate(self):
        pass

    def format(self):
        pass

    def save(self):
        pass
