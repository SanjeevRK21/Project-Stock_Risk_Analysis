import yfinance as yf
import pandas as pd

def load_price_data(ticker: str, start: str, end: str) -> pd.Series:
    """
    Fetch adjusted close price data for a given stock and time range.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)
    
    if data.empty:
        raise ValueError("No data fetched. Check ticker or date range.")
    
    prices = data["Close"].dropna()
    return prices
