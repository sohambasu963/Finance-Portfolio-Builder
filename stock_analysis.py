import yfinance as yf
import pandas as pd
import numpy as np
import concurrent.futures
import time
import tkinter as tk
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'
show_time = False

if show_time: start_time = time.time()
# symbol = AAPL
def get_data(df, stock, rf_rate):
    ticker = yf.Ticker(stock)
    historical_data = ticker.history(period='10y')
    info = ticker.info
    
    if 'currentPrice' in info.keys():
        df.loc[stock]['Price'] = info['currentPrice']
    if 'forwardPE' in info.keys():
        df.loc[stock]['Forward PE'] = info['forwardPE']
    if 'dividendYield' in info.keys():
        df.loc[stock]['Dividend Yield'] = info['dividendYield']
    if 'beta' in info.keys():
        df.loc[stock]['Beta'] = info['beta']
    if 'targetMeanPrice' in info.keys():
        df.loc[stock]['Target Price'] = info['targetMeanPrice']

    returns = historical_data['Close'].pct_change()
    st_dev = np.std(returns) * np.sqrt(252)
    avg_return = returns.mean() * 252
    df.loc[stock]['Average Return'] = avg_return
    df.loc[stock]['Average Volatility'] = st_dev
    df.loc[stock]['Sharpe Ratio'] = (avg_return - rf_rate) / st_dev

def store_data():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0].loc[:, ['Symbol']].set_index('Symbol')
    len_df = len(df)

    rf_rate = yf.Ticker("^TNX").history(period="1y")['Close'].mean() / 100

    df['Average Return'] = [None] * len_df
    df['Average Volatility'] = [None] * len_df
    df['Sharpe Ratio'] = [None] * len_df

    df['Price'] = [None] * len_df
    df['Forward PE'] = [None] * len_df
    df['Dividend Yield'] = [None] * len_df
    df['Beta'] = [None] * len_df
    df['Target Price'] = [None] * len_df

    tickers = df.index.tolist()

        
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for ticker in tickers:
            executor.submit(get_data, df, ticker, rf_rate)

    df['Beta'].fillna(1, inplace=True)
    df.fillna(0, inplace=True)
    df['low_risk'] = (1 / df['Average Volatility']) * (1 / df['Beta']) * df['Dividend Yield']
    df['high_return'] = df['Average Return'] * 0.5 + df['Sharpe Ratio'] * 0.2 + (1 / df['Forward PE']) * 0.2 + df['Beta'] * 0.1

    df.sort_values(by='low_risk', ascending=False, inplace=True)
    low_risk_stocks = df.head(10).index.tolist()

    df.sort_values(by='high_return', ascending=False, inplace=True)
    df['high_return'] = df['high_return'].replace(np.inf, np.nan)
    df.dropna(subset=['high_return'], inplace=True)
    high_return_stocks = df.head(10).index.tolist()

    df.to_csv('stock_data.csv')



if show_time:
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time is {elapsed_time:.2f} seconds")