import yfinance as yf

class InvalidTicker(Exception):
    def __init__(self, message="Invalid ticker symbol or no data available."):
        super().__init__(message)

def ensure_ticker_is_valid(ticker: str) -> yf.Ticker:
    try:
        ticker = yf.Ticker(ticker)
        data = ticker.history(period="1d")
    except Exception as e:
        raise InvalidTicker()
    else:
        if data.empty:
            raise InvalidTicker()
        else:
            return ticker
