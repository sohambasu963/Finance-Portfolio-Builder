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


# Need to add a second df to store the performance data

def get_performance(df, symbol, ticker):
    start_date = "2018-01-01"
    end_date = "2023-01-01"
    
    historical_data = ticker.history(start=start_date, end=end_date)
    total_return = (historical_data['Close'][-1] - historical_data['Close'][0]) / historical_data['Close'][0]
    avg_return = (1 + total_return) ** (1 / 5) - 1
    volatility = np.std(historical_data['Close'].pct_change()) * np.sqrt(252)
    sharpe_ratio = avg_return / volatility

    df.loc[symbol]['total_return'] = total_return
    df.loc[symbol]['avg_return'] = avg_return
    df.loc[symbol]['volatility'] = volatility
    df.loc[symbol]['sharpe_ratio'] = sharpe_ratio
    


def get_historical_data(df, symbol, ticker):
    start_date = "2013-01-01"
    end_date = "2018-01-01"

    historical_data = ticker.history(start=start_date, end=end_date)
    info = ticker.info
    
    if 'forwardPE' in info.keys():
        df.loc[symbol]['forward_pe'] = info['forwardPE']
    if 'dividendYield' in info.keys():
        df.loc[symbol]['div_yield'] = info['dividendYield']
    if 'beta' in info.keys():
        df.loc[symbol]['beta'] = info['beta']

    daily_returns = historical_data['Close'].pct_change()
    df.loc[symbol]['avg_return'] = daily_returns.mean() * 252
    df.loc[symbol]['volatility'] = np.std(daily_returns) * np.sqrt(252)
    df.loc[symbol]['price'] = round(historical_data['Close'][-1], 2)

def store_data():
    rf_rate = yf.Ticker("^TNX").history(period="1y")['Close'].mean() / 100

    table = pd.read_html(SP500_DATA_URL)
    df = table[0].loc[:, ['Symbol']].set_index('Symbol')
    df_len = len(df)

    df['avg_return'] = [None] * df_len
    df['volatility'] = [None] * df_len
    df['sharpe_ratio'] = [None] * df_len
    df['price'] = [None] * df_len
    df['forward_pe'] = [None] * df_len
    df['div_yield'] = [None] * df_len
    df['beta'] = [None] * df_len
    stock_symbols = df.index.tolist()

    performance_df = table[0].loc[:, ['Symbol']].set_index('Symbol')
    performance_df['total_return'] = [None] * df_len
    performance_df['avg_return'] = [None] * df_len
    performance_df['volatility'] = [None] * df_len
    performance_df['sharpe_ratio'] = [None] * df_len


    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for symbol in stock_symbols:
            executor.submit(get_historical_data, df, symbol, yf.Ticker(symbol.replace(".", "-")))
            executor.submit(get_performance, performance_df, symbol, yf.Ticker(symbol.replace(".", "-")))

    df['beta'].fillna(1, inplace=True)
    df.fillna(0, inplace=True)
    df['sharpe_ratio'] = (df['avg_return'] - rf_rate) / df['volatility']
    df.to_csv("./data/" + "stock_data" + ".csv")

    # remove rows with missing data
    performance_df.fillna(0, inplace=True)
    performance_df.to_csv("./data/" + "performance_data" + ".csv")

def print_time():
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time is {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    store_data()
    if SHOW_TIME: print_time()