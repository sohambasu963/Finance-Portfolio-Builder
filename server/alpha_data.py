import os
import requests
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import time

load_dotenv(".env.local")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SP500_DATA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
TSX60_DATA_URL = 'https://en.wikipedia.org/wiki/S%26P/TSX_60'

def scrape_tickers(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip().replace(".", "-")
        tickers.append(ticker)
    return tickers

def get_stock_data(ticker, interval='daily', outputsize='full'):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    if interval == 'daily':
        data, _ = ts.get_daily_adjusted(symbol=ticker, outputsize=outputsize)
    elif interval == 'weekly':
        data, _ = ts.get_weekly_adjusted(symbol=ticker)
    elif interval == 'monthly':
        data, _ = ts.get_monthly_adjusted(symbol=ticker)
    return data

def calculate_metrics(ticker_data):
    daily_returns = ticker_data['5. adjusted close'].pct_change().dropna()
    avg_return = daily_returns.mean()
    volatility = daily_returns.std()
    rf_rate = 0.045
    sharpe_ratio = (avg_return - rf_rate) / volatility
    return avg_return, volatility, sharpe_ratio

def get_stock_metrics(ticker):
    try:
        ticker_data = get_stock_data(ticker)
        avg_return, volatility, sharpe_ratio = calculate_metrics(ticker_data)
        time.sleep(1.1)
        return {
            'Ticker': ticker,
            'Average Return': avg_return,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio,
        }
    except Exception as e:
        if ".TRT" not in ticker:
            return get_stock_metrics(ticker + ".TRT")
        else: 
            print(f"Error fetching data for {ticker}: {e}")


def main():
    sp500_tickers = scrape_tickers(SP500_DATA_URL)
    tsx60_tickers = scrape_tickers(TSX60_DATA_URL)
    all_tickers = sp500_tickers + tsx60_tickers

    with ThreadPoolExecutor(max_workers=3) as executor:
        stock_metrics = list(executor.map(get_stock_metrics, all_tickers))

    # stock_metrics = [metric for metric in stock_metrics if metric is not None]
    stock_metrics = [metric for metric in stock_metrics if metric is not None]
    stock_metrics_df = pd.DataFrame(stock_metrics).dropna().sort_values(by="Sharpe Ratio", ascending=False)
    stock_metrics_df.to_csv('../data/stock_metrics.csv', index=False)
    return stock_metrics_df

if __name__ == "__main__":
    start = time.time()
    result_df = main()
    print(result_df)
    print(f"Time taken: {time.time() - start} seconds")

