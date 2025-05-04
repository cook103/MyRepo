import pandas as pd
import json
import sys
import os
from typing import Dict, Union
sys.path.append(os.path.abspath("../"))
import utils

class DCFModel:
    # perpetual growth rate
    PERP_GROWTH_RATE = 0.03
    # discount rate
    DC_RATE = 0.08

    def __init__(self, ticker: str, growth_rate: Union[int, float] = None):
        self.ticker = ticker.upper()
        if self.ticker in utils.cache_storage:
            # dont make requests, use cached data
            yfinance_ticker_obj = utils.cache_storage[self.ticker]["yf_ticker_obj"]
            self.ticker_info = utils.cache_storage[self.ticker]["ticker_info"]
            self.ticker_balance_sheet = utils.cache_storage[self.ticker]["ticker_balance_sheet"]
            self.ticker_cash_flow = utils.cache_storage[self.ticker]["ticker_cash_flow"]
        else:
            yfinance_ticker_obj = utils.ensure_ticker_is_valid(self.ticker)
            self.ticker_info = yfinance_ticker_obj.info
            self.ticker_balance_sheet = yfinance_ticker_obj.balance_sheet
            self.ticker_cash_flow = yfinance_ticker_obj.cash_flow

            utils.cache_storage[self.ticker] = {
                "yf_ticker_obj": yfinance_ticker_obj,
                "ticker_info": self.ticker_info,
                "ticker_balance_sheet": self.ticker_balance_sheet,
                "ticker_cash_flow": self.ticker_cash_flow,
            }

        self.all_cash_flows_py = None

        if growth_rate is not None:
            if isinstance(growth_rate, (int, float)):
                self.growth_rate = growth_rate / 100
            else:
                raise ValueError("Growth rate must be a number (int or float).")
        else:
            # calculate average growth rate
            self.all_cash_flows_py = self.get_all_cash_flows_per_year()
            self.growth_rate = self.calculate_cash_flow_growth_yoy()



    def calculate_cash_flow_growth_yoy(self) -> float:
        growth_lst = []
        for i in range(0, len(self.all_cash_flows_py) - 1):
            # formula for calculating cash flow growth each year
            growth = (
                self.all_cash_flows_py[i][1] - self.all_cash_flows_py[i + 1][1]
            ) / self.all_cash_flows_py[i + 1][1]
            # add growth for that year to the list
            growth_lst.append(growth)

        # get average growth rate over past 3 years
        avg_growth_rate = sum(growth_lst) / len(growth_lst)

        print(
            f"Using Average cash flow growth rate over last {len(self.all_cash_flows_py)} years: {avg_growth_rate * 100}%"
        )

        return avg_growth_rate


    def get_all_cash_flows_per_year(self) -> list:
        cash_flow_per_year_lst = []

        for year in self.ticker_cash_flow:
            # get the cash flow given the year
            cash_flow_year_tup = (
                str(year),
                self.ticker_cash_flow[year].get("Free Cash Flow"),
            )

            # if the cash flow exists
            if pd.notna(cash_flow_year_tup[1]):
                # add (year, cf) tuple to the list
                cash_flow_per_year_lst.append(cash_flow_year_tup)

        return cash_flow_per_year_lst


    def calculate_future_free_cash_flow(self, p_last_years_cash_flow: int) -> list:
        ffcf_lst = []

        next_year_ffcf = p_last_years_cash_flow * (1 + self.growth_rate)
        ffcf_lst.append(next_year_ffcf)

        future_years = 8
        # Generate 8 more years' worth of future free cash flows
        for _ in range(future_years):
            # Calculate the next ffcf
            ffcf = next_year_ffcf * (1 + self.growth_rate)

            # Append the calculated free cash flow to the list
            ffcf_lst.append(ffcf)

            # Update next year's free cash flow for the next iteration
            next_year_ffcf = ffcf

        # last future free cash flow in list
        last_calculated_ffcf = ffcf_lst[-1]

        # formula to calculate the future free cash flow terminal value
        ffcf_terminal_value = (
            last_calculated_ffcf * \
            (1 + self.PERP_GROWTH_RATE) / (self.DC_RATE - self.PERP_GROWTH_RATE)
        )

        # add terminal value to the end of ffcf list
        ffcf_lst.append(ffcf_terminal_value)

        return ffcf_lst


    def calculate_present_value_ffcf(self, p_future_free_cash_flow_lst) -> list:
        # formula to calculate present value free cash flow per year
        pv_future_free_cash_flow_lst = []
        for year, t_ffcf_py in enumerate(p_future_free_cash_flow_lst):
            year += 1
            if year == 10:
                # skip we will calculate terminal value for the 10th year
                break
            else:
                pv_ffcf = t_ffcf_py / (1 + self.DC_RATE) ** year
                pv_future_free_cash_flow_lst.append(pv_ffcf)

        # calculate present value terminal value
        pv_future_free_cash_flow_lst.append(
            p_future_free_cash_flow_lst[-1] / (1 + self.DC_RATE) ** 10
        )

        return pv_future_free_cash_flow_lst


    def get_discounted_cashflow_pps(self) -> float: 
        # get current stock price
        current_stock_price = self.ticker_info["currentPrice"]

        # current years balance sheet
        current_year = self.ticker_balance_sheet.columns[0]
        
        # cash and cash equivalents
        cash_and_cash_eqv = self.ticker_balance_sheet[current_year]["Cash And Cash Equivalents"]

        # get list of cash flows per year
        if self.all_cash_flows_py is None:
            self.all_cash_flows_py = self.get_all_cash_flows_per_year()

        # calculate future free cash flows
        future_free_cash_flows = self.calculate_future_free_cash_flow(
            self.all_cash_flows_py[0][1]
        )

        # calculate present value of those ffcf's
        present_val_future_free_cash_flows = self.calculate_present_value_ffcf(
            future_free_cash_flows
        )

        # calculate sum of future free cash flows
        sum_of_pv_ffcf = sum(present_val_future_free_cash_flows)

        # calculate equity value
        equity_value = sum_of_pv_ffcf + cash_and_cash_eqv \
            - self.ticker_balance_sheet[current_year]["Total Debt"]

        # discounted cash flow price per share
        dcf_pps = equity_value / self.ticker_info["impliedSharesOutstanding"]

        return round(dcf_pps, 2)


    def run_model(self) -> Dict[str, Union[str, int, float]]:
        # get current stock price
        current_stock_price = self.ticker_info["currentPrice"]

        # calculate intrinsic valueV
        estimated_intrinsic_value = self.get_discounted_cashflow_pps()

        # Anonymous helper function to check valuation
        over_or_under_valued = lambda curr_price, intr_val : \
            "Overvalued" if curr_price > intr_val else "Undervalued"

        # Anonymous helper function to apply margin of safety
        apply_margin_of_safety = lambda dcf_pps, mos: round(dcf_pps * (1 - mos), 2)

        dcf_details_dict = {
            "ticker": self.ticker_info["symbol"],
            "growth_rate_suggestion": self.growth_rate * 100,
            "over_undervalued": over_or_under_valued(current_stock_price, estimated_intrinsic_value),
            "current_price": current_stock_price,
            "wall_street_estimate": self.ticker_info["targetMeanPrice"],
            "intrinsic_value": estimated_intrinsic_value,
        }

        # margins to compare dcf intrinsic value to
        margins_of_safety_to_calculate = [10, 15, 20, 25, 30, 35, 40]

        margin_estimates = {}
        for mos in margins_of_safety_to_calculate:
            margin_estimates[f"{mos}%"] = apply_margin_of_safety(estimated_intrinsic_value, mos/100)

        dcf_details_dict["intrinsic_value_with_mos"] = margin_estimates

        return dcf_details_dict
