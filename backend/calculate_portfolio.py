import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_historical_data(tickers):
    price_data = None

    for ticker in tickers:
        # Fetch historical stock data using AlphaVantage API
        API = "https://www.alphavantage.co/query"
        API_FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"
        API_URL = f"{API}?function={API_FUNCTION}&symbol={ticker}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(API_URL)
        data = response.json()

        # Process historical data
        time_series = data.get('Time Series (Daily)')
        if time_series:
            historical_data = []
            for date, values in time_series.items():
                adjusted_close = float(values['5. adjusted close'])
                historical_data.append((date, adjusted_close))

            historical_data = sorted(historical_data, key=lambda x: x[0])
            ticker_price_data = pd.DataFrame(historical_data, columns=["Date", ticker]).set_index("Date")

            if price_data is None:
                price_data = ticker_price_data
            else:
                price_data = price_data.merge(ticker_price_data, left_index=True, right_index=True, how="outer")

    return price_data


def get_rf_rate():
    API = "https://www.alphavantage.co/query"
    API_FUNCTION = "FEDERAL_FUNDS_RATE"
    API_URL = f"{API}?function={API_FUNCTION}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
    
    response = requests.get(API_URL)
    data = response.json()
    recent_rate = float(data['data'][0]['value'])
    risk_free_rate = (1 + recent_rate / 100) ** (1 / 252) - 1
    
    return risk_free_rate


def get_portfolio(stocks):
    tickers = [stock['symbol'] for stock in stocks]
    price_data = get_historical_data(tickers)

    daily_returns = price_data.pct_change().dropna()
    avg_return = daily_returns.mean()
    volatility = daily_returns.std()
    risk_free_rate = get_rf_rate()
    sharpe_ratio = (avg_return - risk_free_rate) / volatility

    metrics = pd.DataFrame({
        'symbol': tickers,
        'average_return': avg_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    })

    return metrics


