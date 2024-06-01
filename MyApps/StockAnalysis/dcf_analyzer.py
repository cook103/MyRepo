import yfinance as yf
import pandas as pd
import math
import argparse

# perpetual growth rate
PERP_GROWTH_RATE = 0.025

# discount rate
DC_RATE = 0.08

def get_all_cash_flows_per_year(p_cash_flow: dict) -> list:
    cash_flow_per_year_lst = []

    for year in p_cash_flow:
        # get the cash flow given the year
        cash_flow_year_tup = (
            str(year),
            p_cash_flow[year].get("Free Cash Flow"),
        )

        # if the cash flow exists
        if pd.notna(cash_flow_year_tup[1]):
            # add (year, cf) tuple to the list
            cash_flow_per_year_lst.append(cash_flow_year_tup)

    return cash_flow_per_year_lst


def calculate_cash_flow_growth_yoy(p_cash_flow_per_year_lst: list) -> list:
    growth_lst = []
    for i in range(0, len(p_cash_flow_per_year_lst) - 1):
        # formula for calculating cash flow growth each year
        growth = (
            p_cash_flow_per_year_lst[i][1] - p_cash_flow_per_year_lst[i + 1][1]
        ) / p_cash_flow_per_year_lst[i + 1][1]
        # add growth for that year to the list
        growth_lst.append(growth)

    # get average growth rate over past 3 years
    avg_growth_rate = math.fsum(growth_lst) * 100

    print(
        f"Using Average cash flow growth rate over last {len(p_cash_flow_per_year_lst)} years: {round(avg_growth_rate, 3)}%"
    )

    return avg_growth_rate


def calculate_future_free_cash_flow(
    p_cash_flow_per_year_lst: list, p_avg_growth_rate=10
) -> list:
    future_free_cash_flow_lst = [
        t_cf_py[1] * (1 + p_avg_growth_rate)
        for t_cf_py in p_cash_flow_per_year_lst
    ]

    # last future free cash flow in list
    last_calculated_ffcf = future_free_cash_flow_lst[-1]

    # formula to calculate the future free cash flow  terminal value
    ffcf_terminal_value = (
        last_calculated_ffcf
        * (1 + PERP_GROWTH_RATE)
        / (DC_RATE - PERP_GROWTH_RATE)
    )

    # add terminal value to the end of ffcf list
    future_free_cash_flow_lst.append(ffcf_terminal_value)

    return future_free_cash_flow_lst


def calculate_present_value_ffcf(p_future_free_cash_flow_lst) -> list:
    # formula to calculate present value free cash flow per year (year, pv_ffcf) tuple
    pv_future_free_cash_flow_lst = [
        t_ffcf_py / (1 + DC_RATE) ** year
        for year, t_ffcf_py in enumerate(p_future_free_cash_flow_lst, start=1)
    ]
    return pv_future_free_cash_flow_lst


def get_discounted_cashflow_pps(
    p_present_value_ffcf_lst: list,
    p_cash_and_cash_eqv,
    p_total_debt,
    p_shares_outstanding,
) -> float:
    # calculate sum of future free cash flows
    sum_of_pv_ffcf = sum(p_present_value_ffcf_lst)

    # calculate equity value
    equity_value = sum_of_pv_ffcf + p_cash_and_cash_eqv - p_total_debt

    # discounted cash flow price per share
    dcf_pps = equity_value / p_shares_outstanding

    return dcf_pps


def main():
    # create argument parser obj
    parser = argparse.ArgumentParser(description="Fetch Stock Ticker Symbol")

    # add positional argument ticker
    parser.add_argument(
        "ticker", type=str, help="Ticker symbol of company on NYSE"
    )

    # add positional argument avg growth rate
    parser.add_argument(
        "-g", "--growth", type=float, help="Amount of YOY growth you assume"
    )

    # parse command line
    args = parser.parse_args()

    try:
        # stock to dcf analyze
        stock_ticker = yf.Ticker(args.ticker)
    except Exception:
        raise Exception(f"Could not find ticker symbol {args.ticker}")

    # get cash flow
    cash_flow = stock_ticker.cashflow

    # get balance sheet
    company_balance_sheet = stock_ticker.balancesheet

    # most recent year in data
    most_recent_year = company_balance_sheet.columns[0]

    # total debt of the company
    total_debt = company_balance_sheet[most_recent_year]["Total Debt"]

    # cash and cash equivalents
    cash_and_cash_eqv = company_balance_sheet[most_recent_year][
        "Cash And Cash Equivalents"
    ]

    # total company shares outstanding
    shares_outstanding = stock_ticker.info["sharesOutstanding"]

    # get list of cash flows per year
    cash_flows_per_year = get_all_cash_flows_per_year(cash_flow)

    # calculate avg growth on cash flows per year
    if not args.growth:
        avg_cash_flow_growth_rate = calculate_cash_flow_growth_yoy(
            cash_flows_per_year
        )
    else:
        avg_cash_flow_growth_rate = args.growth

    # calculate future free cash flows
    future_free_cash_flows = calculate_future_free_cash_flow(
        cash_flows_per_year, p_avg_growth_rate=avg_cash_flow_growth_rate / 100
    )

    # calculate present value of those ffcf's
    present_val_future_free_cash_flows = calculate_present_value_ffcf(
        future_free_cash_flows
    )

    # calculate intrinsic value
    estimated_intrinsic_value = get_discounted_cashflow_pps(
        present_val_future_free_cash_flows,
        cash_and_cash_eqv,
        total_debt,
        shares_outstanding,
    )

    apply_margin_of_safety = lambda dcf_pps: dcf_pps * (1 - 0.1)
    estimated_intrinsic_value_w_margin_of_safety = apply_margin_of_safety(
        estimated_intrinsic_value
    )

    print("Estimated intrinsic value: ", estimated_intrinsic_value)
    print(
        f"Estimated intrinsic value with margin of safety: {estimated_intrinsic_value_w_margin_of_safety}"
    )


if __name__ == "__main__":
    main()
