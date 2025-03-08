#!/usr/bin/env python3
# import requests
import sys
import os
from flask import Flask, render_template, json, request

# add dcf path & tool
sys.path.append(os.path.abspath("../../MyApps/StockAnalysis"))
try:
    from DCFAnalyzer.dcf_analyzer import DCFModel
except Exception as e:
    print(f"Failed to import DCFModel, error {e}.")
    sys.exit(1)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def return_index():
    """Onload data is sent here"""
    reply_message = {}
    if request.method == "POST":
        if request.form.get("ticker") and request.form.get("rate"):
            ticker = request.form.get("ticker")
            rate =request.form.get("rate")
            
            try:
                rate = float(rate)
            except ValueError:
                reply_message = {"error": "growth rate must be a number."}
                
            try:
                reply_message = DCFModel(ticker, rate).run_model()
            except Exception as e:
                reply_message = {"error": e}

            return render_template("dcf.html", reply_message=reply_message)
        else:
            reply_message= {"error": "Please fill in all required fields."}
            return render_template("dcf.html", reply_message=reply_message)
            
def main():
    app.run(debug=True, host="0.0.0.0", port="8081")

if __name__ == "__main__":
    main()
