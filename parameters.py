parameters = {
        # General parameters
        "model_names":["regressor", "Transformer", "GaussianProcess"],
        "prediction_types":["BB", "BQ", "Bp"],
        "RunOnCluster":False,
        "mode":0, # 0: Training only
                  # 1: Predictions only
                  # 2: Training and Predictions
                  # 3: Models Analysis (on existing models)
                  # 4: Training + Analysis

        # Training Data Parameters
        "dataType":"H5",
        "Data_path":"DATA/yolo.h5",
        "SetName":"BJ2_PQS_0p2",
        "pTCuttOff":[0.2,3],
        "centralities":[0., 10., 20., 40., 60, 80.],
        # Check centralities consistency between parameters and init conditions

        # Ridge Regressor
        "Polydegree":2,
        "RidgeAlpha":0.2,

        #TransformerParameters
        "nhead":1,
        "num_layers":6,
        "dim_feeforward":1024,
        "dropout":0.1,
        "batch_size":128,
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