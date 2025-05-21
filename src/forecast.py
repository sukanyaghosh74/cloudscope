import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_next_month(df: pd.DataFrame):
    df = df.groupby("Date")["Cost"].sum().reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")

    df['day_num'] = (df['Date'] - df['Date'].min()).dt.days
    X = df[['day_num']]
    y = df['Cost']

    model = LinearRegression()
    model.fit(X, y)

    next_day = df['day_num'].max() + 30
    forecast_cost = model.predict([[next_day]])[0]

    return round(forecast_cost, 2)
