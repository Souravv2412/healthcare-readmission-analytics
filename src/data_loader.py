# src/data_loader.py
import pandas as pd
from .config import RAW_DATA

def load_raw_data():
    df = pd.read_csv(RAW_DATA)
    print(f"Shape: {df.shape}")
    return df