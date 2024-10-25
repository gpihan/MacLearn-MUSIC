parameters = {
        ###############################################################
        # General parameters ##########################################
        "RunningMode":0, # 0: Training mode
                        # 1: Predictions mode
                        # 2: TESTS
                        # 3: Analysis mode (on existing models)

        "PossibleNuclei":["Ru", "Zr", "Au"],

        "verbose":True,

        ################################################################
        # Prediction Parameters ########################################

        "PredictionMode":1, # 0, The initial conditions are generated. 
                            # 1, The initial conditions are used from 
                            # InitFolder
        "ModelNames":["RidgeRegressorAuAu_BB"],
        # Models in /TrainedModels on which to perform predictions.

        "PredictionOn":["B", "Q"],

        # If mode 0
        "InitialConditions":"3DMCGlauber",
        "OutputFolder":"TEST",
        "Nev":10,

        # If mode 1        
        "InitFolder":"TEST",
        "PredictOutputPath":"TEST",
        "InitReadType":"3DMCGlauber",

        ################################################################
        ################################################################
        # Training Data Parameters #####################################

        "ModelTypes":["RidgeRegressor"],
        "DataPath":"TrainingData/AuAu",
        "TrainingFnames":["DICT_Au_19.dat", "DICT_Au_200.dat"],

        # Contain nucleus name and energy to help for classification in training.
        # Must corresponds to the content of the files in TrainingFnames 
        "DataInformation":[["Au", 19.6], ["Au", 200]],

        # if read with .h5 files 
        "pTCuttOff":[0.2, 3],
        "centralities":[0., 10., 20., 40., 60, 80.],
        # Check centralities consistency between parameters and init conditions

        # Features parameters
        "FeaturesType":3, # Feature type corresponds to the type of features for the classification
                          # 0, no features, no classification of training data
                          # 1, the training data is split in nucleus
                          # 2, the training data is split in energy
                          # 3, the training data is split in nucleus and energy

        # Smoothing data for training
        "GaussianSmoothingSigma":3,

        "InputCharge":"B",
        "OutputCharge":"B",
        # Possible input charge: "B" and "Q"
        # Possible output charge: "B", "Q", "NetProton", "NetNeutron", "Protons", "Neutrons"

        ################################################################
        ################################################################
        # Analysis parameters ##########################################
        # During the training, the performance of the model can be evaluated.
        # During the prediction, custom analysis can be performed.
        "AnalysisMode":1, # 0, No analysis performed
                          # 1, perform training/prediction analysis 
        
        # The AnalysisOn corresponds to the analysis one wants to perform
        "AnalysisOnTrain":"Full",
        "AnalysisOnPred":"Full",
        "DoPlots":False,

        #################################################################
        # Ridge Regressor
        "PolyDegree":2,
        "RidgeAlpha":0.2,

        ##################################################################
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
