from flask import Flask, jsonify, request
from flask_cors import CORS
from calculate_portfolio import get_portfolio
from dotenv import load_dotenv
import os
import requests

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

@app.route('/search', methods=['GET'])
def search(search_term):
    function = 'SYMBOL_SEARCH'

    response = requests.get(
        f"{API_URL}?function={function}&keywords={search_term}&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    data = response.json()

    if "bestMatches" not in data:
        print("Invalid API response:", data)
        return []

    # Extract stock suggestions from the API response
    suggestions = [
        {
            "symbol": item["1. symbol"],
            "name": item["2. name"],
            "currency": item["8. currency"],
        }
        for item in data["bestMatches"]
        if item["8. currency"] in ["USD", "CAD"]
    ]

    return jsonify(suggestions)


@app.route('/quote', methods=['GET'])
def get_quote(suggestion):
    quote_function = 'GLOBAL_QUOTE'
    overview_function = 'OVERVIEW'

    quote_response = requests.get(
        f"{API_URL}?function={quote_function}&symbol={suggestion['symbol']}&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    quote_data = quote_response.json()

    overview_response = requests.get(
        f"{API_URL}?function={overview_function}&symbol={suggestion['symbol'].split('.')[0]}&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    overview_data = overview_response.json()

    stock_data = {
        "symbol": suggestion["symbol"],
        "name": suggestion["name"],
        "price": round(float(quote_data["Global Quote"]["05. price"]), 2),
        "currency": suggestion["currency"],
        "percentChange": round(float(quote_data["Global Quote"]["10. change percent"].rstrip("%")), 2),
        "dividendYield": round(float(overview_data["DividendYield"]) * 100, 2) if overview_data["DividendYield"] else "N/A",
        "peRatio": round(float(overview_data["PERatio"]), 2) if overview_data["PERatio"] and overview_data["PERatio"] != "None" else "N/A",
        "beta": round(float(overview_data["Beta"]), 2) if overview_data["Beta"] else "N/A",
    }

    return jsonify(stock_data)


@app.route('/performance', methods=['GET'])
def get_performance_data(symbol):
    function = 'TIME_SERIES_DAILY_ADJUSTED'

    response = requests.get(
        f"{API_URL}?function={function}&symbol={symbol}&outputsize=compact&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    data = response.json()

    if "Time Series (Daily)" not in data:
        print("Invalid API response:", data)
        return []

    time_series_data = data["Time Series (Daily)"]

    dates = list(time_series_data.keys())
    adjusted_closing_prices = [round(float(time_series_data[date]["5. adjusted close"]), 2) for date in dates]

    performance_data = {
        "stock": data["Meta Data"]["2. Symbol"],
        "labels": dates,
        "data": adjusted_closing_prices
    }

    return jsonify(performance_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
