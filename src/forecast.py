import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_cost(df: pd.DataFrame) -> float:
    """
    Forecast the total cost 30 days after the most recent date in the dataset
    using a simple linear regression model.

    Parameters:
    - df (pd.DataFrame): DataFrame with columns 'Date' (datetime or string) and 'Cost' (float)

    Returns:
    - float: Forecasted cost rounded to 2 decimal places
    """

    # Aggregate cost per day and ensure proper datetime format
    df = df.groupby("Date")["Cost"].sum().reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")

    # Convert dates to numeric days since the first date
    df['day_num'] = (df['Date'] - df['Date'].min()).dt.days
    X = df[['day_num']]
    y = df['Cost']

    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Forecast cost 30 days into the future
    next_day = df['day_num'].max() + 30
    forecast = model.predict([[next_day]])[0]

    return round(forecast, 2)
