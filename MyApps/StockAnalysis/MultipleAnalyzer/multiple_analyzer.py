import yfinance as yf
from curl_cffi import requests
import sys
import os
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath("../"))
import utils

class MultipleModel:

    def __init__(self, ticker: str):
        self.ticker = ticker.strip().upper()
        self.session = requests.Session(impersonate="chrome")
        yfinance_ticker_obj = utils.ensure_ticker_is_valid(self.ticker)
        self.ticker_info = yfinance_ticker_obj.info


    def get_earnings_estimates(self):
        url = f"https://finance.yahoo.com/quote/{self.ticker_info['symbol']}/analysis/"

        # Define a User-Agent to simulate a real browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  \
            (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send a GET request with headers
        response = self.session.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the earnings estimate section by data-testid
        earnings_section = soup.find('section', {'data-testid': 'earningsEstimate'})

        # Extract data from the table
        earnings_data = {}

        if earnings_section:
            rows = earnings_section.find_all('tr')

            # Loop through each row in the earnings estimate table
            for row in rows:
                cells = row.find_all('td')
                
                # Check if the row has cells and contains the relevant data
                if len(cells) > 1:  # Make sure the row contains at least two cells
                    key = cells[0].get_text(strip=True)
                    value = cells[3].get_text(strip=True)
                    
                    # Store the data in the earnings_data dictionary
                    earnings_data[key] = float(value)

        return earnings_data


    def get_average_pps(self):
        all_estimates = []
        try:
            ttm_price_to_earnings = self.ticker_info["trailingPE"]
        except KeyError:
            raise ValueError("Failed to get multiple from yfinance.")
        else:
            # calculate price with forward eps
            # E x M = P
            earnings_estimates_map = self.get_earnings_estimates()
            all_estimates.append(ttm_price_to_earnings * earnings_estimates_map["Avg. Estimate"])
            all_estimates.append(ttm_price_to_earnings * earnings_estimates_map["Low Estimate"])
            all_estimates.append(ttm_price_to_earnings * earnings_estimates_map["High Estimate"])

            multiple_pps = sum(all_estimates) / len(all_estimates)

            return round(multiple_pps, 2)


    def run_model(self):
        estimated_intrinsic_value = self.get_average_pps()

        current_stock_price = self.ticker_info["currentPrice"]
        
        # Anonymous helper function to check valuation
        over_or_under_valued = lambda curr_price, intr_val : \
            "Overvalued" if curr_price > intr_val else "Undervalued"
        
        multiple_details_dict = {
            "ticker": self.ticker_info["symbol"],
            "over_undervalued": over_or_under_valued(current_stock_price, estimated_intrinsic_value),
            "current_price": current_stock_price,
            "wall_street_estimate": self.ticker_info["targetMeanPrice"],
            "intrinsic_value": estimated_intrinsic_value
        }

        return multiple_details_dict
