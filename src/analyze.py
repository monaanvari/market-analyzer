import yfinance as yf
import investpy
import pandas as pd
from backtest import run_backtest
from plot import plot_results

# Fetch historical data

df = pd.read_excel('./data/Data.xlsx')
# df = yf.download("AAPL", period="5y", interval="1d")

# Get Apple stock data for the last 5 years
df = investpy.get_stock_historical_data(
    stock='AAPL',
    country='United States',
    from_date='01/01/2010',
    to_date='01/08/2024'
)

df = df[["Close"]]

# Keep only Close prices
df = df[["Close"]]
df.dropna(inplace=True)

# Compute features
df["MA_Short"] = df["Close"].rolling(20).mean()
df["MA_Long"] = df["Close"].rolling(50).mean()
df.dropna(inplace=True)

# Run backtest
results = run_backtest(df)

# Plot results
plot_results(df, results)
