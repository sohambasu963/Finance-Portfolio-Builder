import os
import requests
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange


load_dotenv(".env.local")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API = "https://www.alphavantage.co/query"

def get_rf_rate():
    """
    Fetches the annual risk-free rate from the Alpha Vantage API.
    Returns the daily risk-free rate as a float.
    """
    try:
        API_FUNCTION = "FEDERAL_FUNDS_RATE"
        API_URL = f"{API}?function={API_FUNCTION}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(API_URL)
        data = response.json()
        recent_rate = float(data['data'][0]['value'])
    except Exception as e:
        print(f"An error occurred with getting the RF rate: {e}")
        recent_rate = 0.045

    risk_free_rate = (1 + recent_rate / 100) ** (1 / 252) - 1

    return risk_free_rate

def get_exchange_rate():
    """
    Fetches the exchange rate for USD to CAD from the Alpha Vantage API.
    Returns the exchange rate as a float.
    """
    try:
        fx = ForeignExchange(key=ALPHA_VANTAGE_API_KEY)
        data, _ = fx.get_currency_exchange_rate(from_currency='USD', to_currency='CAD')
        exchange_rate = float(data['5. Exchange Rate'])
    except Exception as e:
        print(f"An error occurred with getting the exchange rate: {e}")
        exchange_rate = 1.35

    return exchange_rate