import os
import requests
import pandas as pd
import numpy as np
import httpx
from scipy.optimize import minimize
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def get_optimal_weights(avg_return, cov_matrix, rf_rate):
    num_assets = len(avg_return)
    initial_weights = np.ones(num_assets) / num_assets

    def objective_function(weights):
        portfolio_return = np.dot(weights, avg_return)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - rf_rate) / portfolio_volatility
        return -sharpe_ratio

    constraints = (
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1},
    )

    bounds = [(0, 1) for _ in range(num_assets)]

    result = minimize(
        objective_function,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    return result.x

async def get_historical_data(tickers):
    price_data = None
    max_retries = 3

    for ticker in tickers:
        retries = 0
        while retries < max_retries:
            try:
                # Fetch historical stock data using AlphaVantage API
                API = "https://www.alphavantage.co/query"
                API_FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"
                API_URL = f"{API}?function={API_FUNCTION}&symbol={ticker}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"

                async with httpx.AsyncClient() as client:
                    response = await client.get(API_URL)
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
                    break
                else:
                    raise ValueError("Invalid data received from API")

            except Exception as e:
                retries += 1
                print(f"Error while fetching data for {ticker}: {e}")
                if retries < max_retries:
                    print(f"Retrying {retries}/{max_retries}...")
                else:
                    print(f"Failed to fetch data for {ticker} after {max_retries} retries.")
                    return None

    return price_data



async def get_rf_rate():
    API = "https://www.alphavantage.co/query"
    API_FUNCTION = "FEDERAL_FUNDS_RATE"
    API_URL = f"{API}?function={API_FUNCTION}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        data = response.json()

    recent_rate = float(data['data'][0]['value'])
    risk_free_rate = (1 + recent_rate / 100) ** (1 / 252) - 1
    
    return risk_free_rate



async def get_portfolio(stocks):
    print(stocks)
    tickers = [stock['symbol'] for stock in stocks]
    price_data = await get_historical_data(tickers)

    daily_returns = price_data.pct_change().dropna()
    avg_return = daily_returns.mean()
    # volatility = daily_returns.std()
    cov_matrix = daily_returns.cov()
    rf_rate = await get_rf_rate()
    # sharpe_ratio = (avg_return - rf_rate) / volatility

    optimal_weights = get_optimal_weights(avg_return, cov_matrix, rf_rate)

    return optimal_weights
