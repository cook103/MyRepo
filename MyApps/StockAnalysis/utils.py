import yfinance as yf
import time
from curl_cffi import requests

# store already requested tickers and info
cache_storage = {}

session = requests.Session(impersonate="chrome")

class InvalidTicker(Exception):
    def __init__(self, message="Invalid ticker symbol or no data available."):
        super().__init__(message)

def ensure_ticker_is_valid(ticker: str, request_timeout=5, retry_attempts=5) -> yf.Ticker:
    for attempt in range(retry_attempts):
        try:
            yf_ticker = yf.Ticker(ticker, session=session)
        except yf.exceptions.YFRateLimitError:
            print("Rate limit hit. Retrying in 5 seconds...")
            time.sleep(request_timeout)
        except Exception as e:
            raise InvalidTicker()
        else:
            return yf_ticker
