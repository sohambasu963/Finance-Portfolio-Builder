from flask import Flask, request, jsonify
from calculate_portfolio import generate_portfolio

app = Flask(__name__)

@app.route('/calculate-portfolio', methods=['POST'])
def calculate_portfolio():
    watchlist = request.json['watchlist']
    portfolio = generate_portfolio(watchlist)
    return jsonify(portfolio)

if __name__ == '__main__':
    app.run()
