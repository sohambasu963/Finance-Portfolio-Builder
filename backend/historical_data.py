import yfinance as yf
import pandas as pd
import numpy as np
import concurrent.futures
import time
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'
SHOW_TIME = True
start_time = time.time()

SP500_DATA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def get_old_data(ticker):
    start_date = "2008-01-01"
    end_date = "2018-01-01"

    if "." in ticker:
        ticker = ticker.replace(".", "-")
    ticker = yf.Ticker(ticker)
    historical_data = ticker.history(start=start_date, end=end_date)
    info = ticker.info
    return historical_data, info

def get_current_data(ticker):
    if "." in ticker:
        ticker = ticker.replace(".", "-")
    ticker = yf.Ticker(ticker)
    historical_data = ticker.history(period='10y')
    info = ticker.info
    return historical_data, info


def get_data(df, stock):
    if "." in stock:
        stock = stock.replace(".", "-")
    ticker = yf.Ticker(stock)
    historical_data = ticker.history(period='10y')
    info = ticker.info
    
    if 'forwardPE' in info.keys():
        df.loc[stock]['forward_pe'] = info['forwardPE']
    if 'dividendYield' in info.keys():
        df.loc[stock]['div_yield'] = info['dividendYield']
    if 'beta' in info.keys():
        df.loc[stock]['beta'] = info['beta']
    if 'targetMeanPrice' in info.keys():
        df.loc[stock]['analyst_target'] = info['targetMeanPrice']

    daily_returns = historical_data['Close'].pct_change()
    df.loc[stock]['avg_return'] = daily_returns.mean() * 252
    df.loc[stock]['volatility'] = np.std(daily_returns) * np.sqrt(252)
    df.loc[stock]['price'] = round(historical_data['Close'][-1], 2)

def store_data():
    table = pd.read_html(SP500_DATA_URL)
    df = table[0].loc[:, ['Symbol']].set_index('Symbol')
    df_len = len(df)

    rf_rate = yf.Ticker("^TNX").history(period="1y")['Close'].mean() / 100

    df['avg_return'] = [None] * df_len
    df['volatility'] = [None] * df_len
    df['sharpe_ratio'] = [None] * df_len

    df['price'] = [None] * df_len
    df['forward_pe'] = [None] * df_len
    df['div_yield'] = [None] * df_len
    df['beta'] = [None] * df_len
    df['analyst_target'] = [None] * df_len

    tickers = df.index.tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for ticker in tickers:
            executor.submit(get_data, df, ticker)

    df['beta'].fillna(1, inplace=True)
    df.fillna(0, inplace=True)
    df['sharpe_ratio'] = (df['avg_return'] - rf_rate) / df['volatility']

    df.to_csv("./data/" + "old_stock_data" + ".csv")

def print_time():
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time is {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    store_data()
    if SHOW_TIME: print_time()