from Model import Model
from sklearn.pipeline import make_pipeline
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import xgboost as xgb
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import mean_squared_error
from scipy.ndimage import gaussian_filter1d






class TransformerRegressor(nn.Module):
    def __init__(self, input_dim, output_dim, nhead=73, num_layers=6, dim_feedforward=1024, dropout=0.1):
        super(TransformerRegressor, self).__init__()
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=input_dim, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.batch_norm = nn.BatchNorm1d(input_dim)
        self.linear = nn.Linear(input_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = x.unsqueeze(0)  # Add batch dimension
        x = self.transformer_encoder(x)
        x = x.squeeze(0)  # Remove batch dimension
        x = self.batch_norm(x)  # Apply batch normalization
        x = self.dropout(x)
        x = self.linear(x)
        return x


class Transformer(Model):
    def __init__(self, Param):
        self.nhead = Param["nhead"]
        self.num_layers = Param["num_layers"]
        self.dim_feedforward = Param["dim_feeforward"]
        self.dropout = Param["dropout"]
        self.batch_size = Param["batch_size"]
        self.epoch = Param["epoch"]
        self.learning_rate = Param["learning_rate"]
        self.early_stopping_patience = Param["early_stopping_patience"]
        self.sigma = Param["sigma"]
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.OptimScheduler_mode = Param["OptimScheduler_mode"]
        self.OptimScheduler_factor = Param["OptimScheduler_factor"]
        self.OptimScheduler_patience = Param["OptimScheduler_patience"]
        self.fname = Param["Output_file_name"]
        self.BatchSize = Param["PredictBatchSize"]
        self.GaussianFilterSigma = Param["GaussianFilterSigma"]

    def train(self, Xtrain, Ytrain, Xtest, Ytest):
        # Convert input arrays into PyTorch Tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        Y_train_tensor = torch.FloatTensor(Y_train).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        Y_test_tensor = torch.FloatTensor(Y_test).to(self.device)

        # Create TensorDataset and DataLoader
        train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
        val_dataset = TensorDataset(X_test_tensor, Y_test_tensor)
        train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_dataloader = DataLoader(val_dataset, batch_size=batch_size)

        # Initialize the model
        self.input_dim = X_train_tensor.shape[1]
        self.output_dim = Y_train_tensor.shape[1]
        model = TransformerRegressor(self.input_dim, self.output_dim).to(self.device)

        # Define optimizer and loss function
        optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
        criterion = nn.SmoothL1Loss()  # Huber loss
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode=self.OptimScheduler_mode, 
                                                         factor=self.OptimScheduler_factor, patience=OptimScheduler_patience, 
                                                         verbose=False)

        # Early stopping
        best_val_loss = float('inf')
        early_stopping_counter = 0
        # Training loop
        for epoch in range(epochs):
            model.train()
            total_loss = 0
            for batch in train_dataloader:
                b_input, b_labels = batch
                b_input = b_input.to(self.device)
                b_labels = b_labels.to(self.device)

                optimizer.zero_grad()
                outputs = model(b_input)
                loss = criterion(outputs, b_labels)
                total_loss += loss.item()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Gradient clipping
                optimizer.step()

            avg_train_loss = total_loss / len(train_dataloader)
            print(f"Epoch {epoch + 1}, Loss: {avg_train_loss}")

            # Validation
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch in val_dataloader:
                    b_input, b_labels = batch
                    b_input = b_input.to(self.device)
                    b_labels = b_labels.to(self.device)

                    outputs = model(b_input)
                    loss = criterion(outputs, b_labels)
                    val_loss += loss.item()

            avg_val_loss = val_loss / len(val_dataloader)
            print(f"Validation Loss: {avg_val_loss}")
            
            # Step with the scheduler
            scheduler.step(avg_val_loss)

            # Early stopping
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                early_stopping_counter = 0
                best_model_state = model.state_dict()
            else:
                early_stopping_counter += 1
                if early_stopping_counter >= early_stopping_patience:
                    print(f"Early stopping triggered at epoch {epoch + 1}")
                    break
        # Load the best model state
        model.load_state_dict(best_model_state)

        # Final validation
        model.eval()
        self.model = model

    def preprocess_data(self, X):
        X_tensor = torch.tensor(X, dtype=torch.float32)
        dataset = TensorDataset(X_tensor, torch.zeros((X.shape[0], self.model.linear.out_features)))
        return dataset

    def predict(self, X): # It may not work with a batch_size > Data size
        dataset = self.preprocess_data(X)
        dataloader = DataLoader(dataset, batch_size=self.BatchSize)
        self.model.eval()
        predictions = []
        with torch.no_grad():
            for batch in dataloader:
                inputs, _ = batch
                inputs = inputs.to(self.model.linear.weight.device)
                outputs = self.model(inputs)
                predictions.append(outputs.cpu().numpy())

        predictions = np.concatenate(predictions, axis=0)
        predictions = gaussian_filter1d(predictions, sigma = self.GaussianFilterSigma)
        return predictions


    def save(self):
        with open(self.fname, 'wb') as f:
            # Save the model
            torch.save({'model_state_dict': self.model.state_dict(),
                'input_dim': self.input_dim, 'output_dim': self.output_dim}, self.fname)


class RidgeRegressor(Model):
    def __init__(self, Param):
        self.pipeline = make_pipeline(
            PolynomialFeatures(degree=Param["Polydegree"]),
            Ridge(alpha=Param["RidgeAlpha"])
        )
        self.fname = Param["Output_file_name"]

    def train(self,  X_train, Y_train, X_test, Y_test):
        self.pipeline.fit(X_train, Y_train)

    def predict(self, Y):
        return self.pipeline.predict(Y)

    def save(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self, f)


class LinearRegressor(Model):
class GaussianProcess(Model):
