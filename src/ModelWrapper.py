

class ModelWrapper():
    def __init__(self, model_type, Nuc="Ru", C="B", model_path=None, nuc_encoder_path=None, charge_encoder_path=None):
        if model_type.lower() == 'linear_regression':
            self.model = LinearRegressionModel()
        elif model_type.lower() == 'ridge_regression':
            self.model = RidgeRegressionModel()
        elif model_type.lower() == 'transformer':
            self.model = TransformerModelWrapper()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.NUC = Nuc
        self.C = C
        self.nuc_list = ["Ru", "Zr"]
        self.c_list = ["B", "Q"]
        if self.NUC not in self.nuc_list:
            self.NUC = "Ru"
        if self.C not in self.c_list:
            self.C = "B"
        

        self.model.load(model_path=model_path, nuc_encoder_path=nuc_encoder_path, charge_encoder_path=charge_encoder_path)

    def predict(self, initial_inputs):
        return self.model.predict(initial_inputs, [self.NUC]*len(initial_inputs), [self.C]*len(initial_inputs))

