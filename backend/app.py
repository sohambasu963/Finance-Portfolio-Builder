from flask import Flask, jsonify, request
from flask_cors import CORS
from calculate_portfolio import get_portfolio

app = Flask(__name__)
CORS(app)

# @app.route('/')
# def home():
#     return jsonify({"message": "Hello, this is a simple endpoint!"})

@app.route('/portfolio', methods=['POST'])
def calculate_portfolio():
    stocks = request.json
    data = get_portfolio(stocks)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
