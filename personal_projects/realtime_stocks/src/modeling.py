from load_data import initialize_project
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import optuna
from sklearn.metrics import mean_squared_error, accuracy_score
import pandas as pd
import pickle
import os

import warnings
warnings.filterwarnings('ignore')

__version__ = '0.1.0'


class Modeling:
    def __init__(self, symbol):
        self.symbol = symbol
        self.df_transposed = initialize_project(symbol)
        self.X = self.df_transposed.drop('close', axis=1)
        self.y = self.df_transposed['close']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)   


    def objective(self, trial):
        # Define hyperparameters to be tuned
        param = {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse',
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'lambda': trial.suggest_loguniform('lambda', 1e-8, 1.0),
            'alpha': trial.suggest_loguniform('alpha', 1e-8, 1.0)
        }

        if param['booster'] == 'gbtree' or param['booster'] == 'dart':
            param['max_depth'] = trial.suggest_int('max_depth', 1, 9)
            param['eta'] = trial.suggest_loguniform('eta', 1e-8, 1.0)
            param['gamma'] = trial.suggest_loguniform('gamma', 1e-8, 1.0)
            param['grow_policy'] = trial.suggest_categorical('grow_policy', ['depthwise', 'lossguide'])

        if param['booster'] == 'dart':
            param['sample_type'] = trial.suggest_categorical('sample_type', ['uniform', 'weighted'])
            param['normalize_type'] = trial.suggest_categorical('normalize_type', ['tree', 'forest'])
            param['rate_drop'] = trial.suggest_loguniform('rate_drop', 1e-8, 1.0)
            param['skip_drop'] = trial.suggest_loguniform('skip_drop', 1e-8, 1.0)

        # Training the model
        model = XGBRegressor(**param, random_state=42)
        model.fit(self.X_train, self.y_train)

        # Predict on validation set and calculate RMSE
        y_pred = model.predict(self.X_test)
        rmse = mean_squared_error(self.y_test, y_pred, squared=False)

        return rmse


    def make_model(self) -> None:
        study = optuna.create_study(direction='minimize')
        study.optimize(self.objective, n_trials=100)
        best_params = study.best_params
        xgb_tuned = XGBRegressor(**best_params, random_state=42)

        models_dir = "../models"
        os.makedirs(models_dir, exist_ok=True)
        
        with open("../models/xgb_reg_model.pkl", "wb") as file:
            pickle.dump(xgb_tuned, file)
    
    def get_model(self):
        model_path = "../models/xgb_reg_model.pkl"
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        
        return model

