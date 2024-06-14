# ------- BEFORE STARTING - SOME BASIC TIPS
# You can add a comment within a Python file by using a hashtag '#'
# Anything that comes after the hashtag on the same line, will be considered
# a comment and won't be executed as code by the Python interpreter.

import pandas as pd
import optuna
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    """
    This function loads in CSV data into a pandas dataframe and drops the unnamed column.
    """
    df = pd.read_csv(path)
    df = df.drop(columns=["Unnamed: 0"], errors='ignore')
    return df

def create_train_test(data: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits predictors and targets, then splits them into training and test sets.
    """
    X = data.drop(target, axis=1)
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    return X_train, X_test, y_train, y_test

def objective(trial, X_train, y_train, X_test, y_test):
    # Define the hyperparameter search space
    n_estimators = trial.suggest_int('n_estimators', 100, 1000)
    max_depth = trial.suggest_int('max_depth', 2, 32, log=True)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
    max_features = trial.suggest_categorical('max_features', ['auto', 'sqrt', 'log2', None])
    
    # Create the model with suggested hyperparameters
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        random_state=42
    )
    
    # Scale data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model.fit(X_train_scaled, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    
    return -mae

def train_model_with_optuna(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> dict:
    # Run the Optuna optimization
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_test, y_test), n_trials=100)
    
    # Retrieve best hyperparameters
    best_params = study.best_params
    
    # Calculate average MAE over all trials
    average_mae = -sum([trial.value for trial in study.trials]) / len(study.trials)
    
    return best_params, average_mae

def main(path: str, target: str):
    # Load data
    data = load_data(path)
    
    # Create train and test sets
    X_train, X_test, y_train, y_test = create_train_test(data, target)
    
    # Optimize hyperparameters and train the model
    best_params, avg_mae = train_model_with_optuna(X_train, X_test, y_train, y_test)
    
    print("Best hyperparameters found: ", best_params)
    print("Average MAE over all trials: ", avg_mae)