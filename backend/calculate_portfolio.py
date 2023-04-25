import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def fetch_data(stocks):
    print("data")

