import yfinance as yf
import pandas as pd
import numpy as np
import concurrent.futures
import time
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'
SHOW_TIME = True
start_time = time.time()

# symbol = AAPL
def get_data(df, stock):
    if "." in stock:
        stock = stock.replace(".", "-")
    ticker = yf.Ticker(stock)
    historical_data = ticker.history(period='10y')
    info = ticker.info
    
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
    df.loc[stock]['Price'] = round(historical_data['Close'][-1], 2)

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
            executor.submit(get_data, df, ticker)

    df['Beta'].fillna(1, inplace=True)
    df.fillna(0, inplace=True)
    df['Sharpe Ratio'] = (df['Average Return'] - rf_rate) / df['Average Volatility']

    df.to_csv("./data/" + "old_stock_data" + ".csv")

def print_time():
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time is {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    store_data()
    if SHOW_TIME: print_time()