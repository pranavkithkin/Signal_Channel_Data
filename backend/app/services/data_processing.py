import os
import pandas as pd

def load_strategy_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    data_path = os.path.join(base_dir, "app", "data", "sessions", "strategies.csv")
    df = pd.read_csv(data_path)
    df['timestamp'] = df['timestamp'].astype(str)  # for JSON serialization
    return df
