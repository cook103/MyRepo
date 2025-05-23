import yfinance as yf
import time
import enum
import threading
from curl_cffi import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

### globals

# const
DAYS_IN_SECONDS = 86400
CACHE_MUTEX = threading.Lock()

# non const
cache_storage = {}
earnings_estimates_cache = {}
session = requests.Session(impersonate="chrome")

class ResetHour(enum.Enum):
    THREE_AM = 3
    SIX_AM = 6
    SIX_PM = 17

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

def start_cache_reset_thread(reset_hour=ResetHour.THREE_AM.value) -> None:
    def reset_cache():
        while True:
            now = datetime.now(ZoneInfo("America/Los_Angeles"))
            next_run = now.replace(hour=reset_hour)

            if now >= next_run:
                next_run += timedelta(days=1)

            sleep_seconds = (next_run - now).total_seconds()
            time.sleep(sleep_seconds)

            with CACHE_MUTEX:
                cache_storage.clear()
                earnings_estimates_cache.clear()

    threading.Thread(target=reset_cache, daemon=True).start()
