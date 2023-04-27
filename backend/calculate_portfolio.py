import os
import requests
import pandas as pd
import numpy as np
import httpx
from scipy.optimize import minimize
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def calculate_shares(portfolio_data, portfolio_value, exchange_rate):
    for stock in portfolio_data:
        if stock['currency'] == 'USD':
            stock['shares'] = round((portfolio_value * stock['weight']) / (stock['price'] * exchange_rate))
            stock['bookValueCAD'] = round(stock['shares'] * stock['price'] * exchange_rate, 2)
            stock['bookValueLocal'] = round(stock['shares'] * stock['price'], 2)
        else:
            stock['shares'] = round((portfolio_value * stock['weight']) / stock['price'])
            stock['bookValueCAD'] = round(stock['shares'] * stock['price'], 2)
            stock['bookValueLocal'] = stock['book_value_cad']
        stock.pop('weight', None)

    return portfolio_data

async def get_exchange_rate():
    API = "https://www.alphavantage.co/query"
    API_FUNCTION = "CURRENCY_EXCHANGE_RATE"
    FROM_CURRENCY = "USD"
    TO_CURRENCY = "CAD"
    API_URL = f"{API}?function={API_FUNCTION}&from_currency={FROM_CURRENCY}&to_currency={TO_CURRENCY}&apikey={ALPHA_VANTAGE_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        data = response.json()

    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return exchange_rate

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

    for ticker in tickers:
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



# async def get_portfolio(stocks):
#     print(stocks)
#     tickers = [stock['symbol'] for stock in stocks]
#     price_data = await get_historical_data(tickers)

#     daily_returns = price_data.pct_change().dropna()
#     avg_return = daily_returns.mean()
#     # volatility = daily_returns.std()
#     cov_matrix = daily_returns.cov()
#     rf_rate = await get_rf_rate()
#     # sharpe_ratio = (avg_return - rf_rate) / volatility

#     optimal_weights = get_optimal_weights(avg_return, cov_matrix, rf_rate)

#     return optimal_weights

async def get_portfolio(stocks):
    tickers = [stock['symbol'] for stock in stocks]
    num_tickers = len(tickers)
    price_data = await get_historical_data(tickers)
    # change this code so that old history for AAPL doesn't get dropped because META is newer
    daily_returns = price_data.pct_change()
    avg_return = daily_returns.mean()
    volatility = daily_returns.std()
    cov_matrix = daily_returns.cov()
    rf_rate = await get_rf_rate()
    optimal_weights = get_optimal_weights(avg_return, cov_matrix, rf_rate)

    portfolio_data = []
    for i in range(num_tickers):
        portfolio_data.append({
            "symbol": tickers[i],
            "name": stocks[i]['name'],
            "price": float(stocks[i]['price']),
            "currency": stocks[i]['currency'],
            "weight": float(optimal_weights[i]),
        })
    portfolio_value = 100000
    exchange_rate = await get_exchange_rate()
    portfolio_data = calculate_shares(portfolio_data, portfolio_value, exchange_rate)
    
    return portfolio_data
