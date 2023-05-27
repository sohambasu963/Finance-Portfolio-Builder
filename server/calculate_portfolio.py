import os
import requests
import pandas as pd
import numpy as np
import httpx
from alpha_vantage.timeseries import TimeSeries
from scipy.optimize import minimize
from dotenv import load_dotenv
from metrics import get_rf_rate, get_exchange_rate

load_dotenv(".env.local")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API = "https://www.alphavantage.co/query"

def calculate_shares(portfolio_data, portfolio_value, exchange_rate):
    for stock in portfolio_data:
        if stock['currency'] == 'USD':
            stock['shares'] = round((portfolio_value * stock['weight']) / (stock['price'] * exchange_rate))
            stock['bookValueCAD'] = round(stock['shares'] * stock['price'] * exchange_rate, 2)
            stock['bookValueLocal'] = round(stock['shares'] * stock['price'], 2)
        else:
            stock['shares'] = round((portfolio_value * stock['weight']) / stock['price'])
            stock['bookValueCAD'] = round(stock['shares'] * stock['price'], 2)
            stock['bookValueLocal'] = stock['bookValueCAD']
        stock.pop('weight', None)

    return portfolio_data


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

    min_weight = 1 / (num_assets * 4)

    bounds = [(min_weight, 1)] * num_assets

    result = minimize(
        objective_function,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    return result.x


def get_historical_data(tickers):
    price_data = None

    for ticker in tickers:
        try:
            ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
            data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            data = data['5. adjusted close'].rename(ticker)
            
            if price_data is None:
                price_data = pd.DataFrame(data)
            else:
                price_data = price_data.merge(data, left_index=True, right_index=True, how="outer")
                
        except Exception as e:
            print(f"An error occurred while fetching historical data for {ticker}: {e}")

    return price_data


def get_portfolio(stocks):
    tickers = [stock['symbol'] for stock in stocks]
    num_tickers = len(tickers)
    price_data = get_historical_data(tickers)

    daily_returns = price_data.pct_change()
    avg_return = daily_returns.mean()
    # volatility = daily_returns.std()
    cov_matrix = daily_returns.cov()
    rf_rate = get_rf_rate()

    print(price_data)
    print(avg_return)
    print(cov_matrix)
    print(rf_rate)

    optimal_weights = get_optimal_weights(avg_return, cov_matrix, rf_rate)
    print(optimal_weights)
    
    portfolio_data = []
    for i in range(num_tickers):
        portfolio_data.append({
            "symbol": tickers[i],
            "name": stocks[i]['name'],
            "price": float(stocks[i]['price']),
            "currency": stocks[i]['currency'],
            "weight": float(optimal_weights[i]),
        })
    portfolio_value = 100_000
    # exchange_rate = get_exchange_rate()
    exchange_rate = 1.35
    portfolio_data = calculate_shares(portfolio_data, portfolio_value, exchange_rate)

    print(portfolio_data)
    
    return portfolio_data
