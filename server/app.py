from flask import Flask, jsonify, request
from flask_cors import CORS
from calculate_portfolio import get_portfolio
from dotenv import load_dotenv
import os
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)

load_dotenv(".env.local")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API_URL = "https://www.alphavantage.co/query"

@app.route('/portfolio', methods=['POST'])
def calculate_portfolio():
    stocks = request.json
    data = get_portfolio(stocks)
    return jsonify(data)

@app.route('/watchlist', methods=['GET'])
def get_watchlist():
    NUM_STOCKS = 5
    TOP_N = 25

    df = pd.read_csv("../data/stock_metrics.csv")
    top_stocks = df.head(TOP_N)
    watchlist_stocks = top_stocks.sample(NUM_STOCKS)
    watchlist_stocks = watchlist_stocks['Ticker'].tolist()

    print(watchlist_stocks)

    return jsonify(watchlist_stocks)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
