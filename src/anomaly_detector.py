import pandas as pd

def detect_anomalies(df: pd.DataFrame, column='Cost', threshold=2.5):
    df['z_score'] = (df[column] - df[column].mean()) / df[column].std()
    df['anomaly'] = df['z_score'].abs() > threshold
    return df
