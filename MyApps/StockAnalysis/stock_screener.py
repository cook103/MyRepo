import yfinance as yf
import pandas as pd
import argparse

SP_500_TICKERS_PATH = "./data/constituents.csv"

def get_tickers_from_csv(file_name: str) -> list:
    df = pd.read_csv(file_name, index_col=None)
    return df["Symbol"].to_list()

def calculate_analyst_yoy_gain_prediction(tickers: list):
    stock_data_lst = []
    for ticker in tickers:
        try:
            stock_ticker = yf.Ticker(ticker)
        except Exception:
            print(f"Could not find ticker symbol {ticker}")
        else:
            stock_info = stock_ticker.info
            stock_curr_price = stock_info.get("currentPrice")
            stock_prediction_price = stock_info.get("targetMeanPrice")

            if stock_curr_price and stock_prediction_price:
                # calculate gain
                estimated_percentage_change = (
                    ((stock_prediction_price - stock_curr_price) / stock_curr_price) * 100
                )

                stock_data_and_estimated_percent_change = (
                    ticker,
                    stock_curr_price,
                    stock_prediction_price,
                    estimated_percentage_change
                )

                stock_data_lst.append(stock_data_and_estimated_percent_change)

    return stock_data_lst

def main():

    parser = argparse.ArgumentParser(
        description="Wallstreet Stock Screener To Analyze % Gain"
    )

    parser.add_argument(
        "percent_growth",
        type=float,
        help="Amount of percentage-gain to filter for"
    )

    args = parser.parse_args()

    sp_500_tickers = get_tickers_from_csv(SP_500_TICKERS_PATH)
    sp_500_anyalyst_predictions = calculate_analyst_yoy_gain_prediction(sp_500_tickers)

    out_file_name = f"analyst_{args.percent_growth}_percent_growth_tickers.txt"

    with open(out_file_name, "w") as f:
        for ticker, stock_price, stock_pred, perc_change in sp_500_anyalyst_predictions:
            if perc_change >= args.percent_growth:
                f.write(f"Ticker: {ticker} has an estimated gain of {perc_change}\n")
    
if __name__ == "__main__":
    main()
