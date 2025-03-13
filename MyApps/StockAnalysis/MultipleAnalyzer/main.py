import argparse
import multiple_analyzer as m_model

def main():
    # create argument parser obj
    parser = argparse.ArgumentParser(description="Multiple stock analyzer")

    # add positional argument ticker
    parser.add_argument("ticker", type=str, help="Ticker symbol of a company")

    # parse command line
    args = parser.parse_args()
    print("End year estimated value: ", m_model.MultipleModel(args.ticker).get_average_price())

if __name__ == "__main__":
    main()
