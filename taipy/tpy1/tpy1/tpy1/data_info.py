import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    # input_name = input("Enter variable name for dataframe: ")
    # globals()[input_name] = pd.read_csv(path)
    # return globals()[input_name]
    return pd.read_csv(path)

def quick_info(path: str) -> None:
    df = load_data(path)
    print(df.info())
    print("="*20)
    print("="*20)
    print(df.describe())
    print("="*20)
    print("="*20)
    print(df.isna().sum())
    print("="*20)
    print("="*20)

print("DATA INFORMATION SUCCESFULLY ACCESSED")


# def main():
#     water_df = load_data("taipy/tpy1/tpy1/data/water.csv")
#     print(water_df.head())

# main()