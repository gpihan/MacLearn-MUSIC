parameters = {
        # General parameters #########################################
        "mode":0, # 0: Training only
                  # 1: Predictions only
                  # 2: Training and Predictions
                  # 3: Models Analysis (on existing models)
                  # 4: Training + Analysis + predictions
        "PossibleNuclei":["Ru", "Zr", "Au"],

        # Prediction Parameters ################################################
        # Models in /TrainedModels on which to perform predictions.
        "ModelNames":["TransformerAuRuZr_BNetProton", "RidgeRegressorAuRuZr_BB"],
        "PredictionOn":["B", "B"],
        "RunOnCluster":False,
        "InitialConditions":"3DMCGlauber",
        "OutputFolder":"AuAu19",
        "Nev":10,


        # Training Data Parameters #####################################
        "DataPath":"TrainingData/AuRuZr",
        "SetName":"BJ2_PQS_0p2",
        "pTCuttOff":[0.2, 3],
        "centralities":[0., 10., 20., 40., 60, 80.],
        "FeaturesType":3, # Feature type corresponds to the type of features for the classification
                          # 0, no features, no classification of training data
                          # 1, the training data is split in nucleus
                          # 2, the training data is split in energy
                          # 3, the training data is split in nucleus and energy
        # Contain nucleus name and energy to help for classification in training.
        # Should have the same size as the number of folder in DataPath.
        # The order is not important.
        "DataInformation":[["Au", 19.6], ["Au", 200]],
        # Check centralities consistency between parameters and init conditions
        "GaussianSmoothingSigma":3,

        
        # Ridge Regressor
        "PolyDegree":2,
        "RidgeAlpha":0.2,

        #TransformerParameters
        "nhead":1,
        "num_layers":6,
        "dim_feeforward":1024,
        "dropout":0.1,
        "BatchSize":128,
        "PredictBatchSize":128,
        "epochs":350,
        "learning_rate":1e-4,
        "early_stopping_patience":15,
        "sigma":3,
        "OptimScheduler_mode":"min",
        "OptimScheduler_factor":0.1,
        "OptimScheduler_patience":5,
        "Output_file_name":"transformer_model.pth",
        "BatchSize":512,
        "GaussianFilterSigma":1.5,
}
