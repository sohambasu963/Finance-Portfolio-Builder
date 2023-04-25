from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/')
# def home():
#     return jsonify({"message": "Hello, this is a simple endpoint!"})

@app.route('/portfolio', methods=['POST'])
def calculate_portfolio():
    stocks = request.json
    print(stocks)
    # Perform your calculations here based on the stock data received
    # This is just an example; modify the logic as needed
    portfolio = []
    for stock in stocks:
        stock_data = {
            "symbol": stock["symbol"],
            "company_name": stock["name"],
            "price": stock["price"],
            "currency": stock["currency"],
            "shares": 10,  # Example calculation; replace with your logic
            "book_value_cad": float(stock["price"]) * 10,  # Example calculation; replace with your logic
            "book_value_local": float(stock["price"]) * 10,  # Example calculation; replace with your logic
        }
        portfolio.append(stock_data)

    return jsonify(portfolio)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
