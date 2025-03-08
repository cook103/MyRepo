import argparse
from dcf_analyzer import DCFModel

def main():
    # create argument parser obj
    parser = argparse.ArgumentParser(description="DCF stock analyzer")

    # add optional argument for verbose mode
    parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="verbose mode: creates a file with more ticker info"
    )

    # add positional argument ticker
    parser.add_argument("ticker", type=str, help="Ticker symbol of a company")


    # add positional argument avg growth rate
    parser.add_argument(
        "-g", "--growth", type=float, help="Growth rate assumptions"
    )

    # parse command line
    args = parser.parse_args()

    if args.growth:
        dcf = DCFModel(args.ticker, args.growth)
    else:
        dcf = DCFModel(args.ticker)

    # create a file with additional information if verbose flag was provided.
    if args.verbose:
        with open("ticker-data.json", "w") as f:
            json.dump(dcf.ticker_info, f, indent=4)

    # run model
    dcf_details_map = dcf.run_model()
    
    # print model predictions
    for k, v in dcf_details_map.items():
        if k == "intrinsic_value_with_mos":
            for percent, price in v.items():
                print(f"Estimated Intrinsic value at {percent} mos: {price}")
        else:
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
