#!/usr/bin/env python3
# import requests
import sys
import os
from flask import Flask, render_template, json, request

# add dcf path & tool
sys.path.append(os.path.abspath("../../MyApps/StockAnalysis"))

try:
    from MultipleAnalyzer.multiple_analyzer import MultipleModel
except Exception as e:
    print(f"Failed to import MultipleModel, error {e}.")
    sys.exit(1)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def return_index():
    reply_message = {}
    if request.method == "POST":
        if request.form.get("ticker"):
            ticker = request.form.get("ticker")
            try:
                reply_message = {
                    "Ticker": ticker,
                    "avgPrice": MultipleModel(ticker).get_average_price()
                }
            except Exception as e:
                reply_message = {"error": e}
        else:
            reply_message= {"error": "Please fill in all required fields."}
    return render_template("multiple.html", reply_message=reply_message)
            
def main():
    app.run(debug=True, host="0.0.0.0", port="8082")

if __name__ == "__main__":
    main()
