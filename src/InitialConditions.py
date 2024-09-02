from src.Init3DMCG import Init3DMCG



class InitialConditions():
    def __init__(self, Param):
        if Param["InitialConditions"] == "3DMCG":
            self.InitialCondition = Init3DMCG()
        # Add initial conditions if new initial conditions codes are available
        # Also add in the .gitmodules

    def generate(self):
        pass

    def format(self):
        pass

    def save(self):
        pass
