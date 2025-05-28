import pandas as pd

def coin_performance(df):
    """Returns average gain per coin."""
    return df.groupby('coin')['gain_pct'].mean().sort_values()

def win_loss_count(df):
    """Returns win/loss/none counts."""
    return df['outcome'].value_counts().to_dict()

# Add more analysis functions as needed