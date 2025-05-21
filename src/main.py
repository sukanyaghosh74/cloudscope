import pandas as pd

def normalize_uploaded_file(df: pd.DataFrame, provider: str) -> pd.DataFrame:
    if provider == "AWS":
        df = df.rename(columns={
            'UsageDate': 'Date',
            'ServiceName': 'Service',
            'BlendedCost': 'Cost'
        })
    elif provider == "Azure":
        df = df.rename(columns={
            'UsageStartTime': 'Date',
            'MeterCategory': 'Service',
            'CostInUSD': 'Cost'
        })
    elif provider == "GCP":
        df = df.rename(columns={
            'Start Time': 'Date',
            'Service Description': 'Service',
            'Cost': 'Cost'
        })
    df = df[['Date', 'Service', 'Cost']]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df = df.dropna()
    return df
