#!/usr/bin/env python3
import sys
import os
import argparse
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.abspath("../../MyApps/StockAnalysis"))

try:
    from DCFAnalyzer.dcf_analyzer import DCFModel
except Exception as e:
    print(f"Failed to import DCFModel, error {e}.")
    sys.exit(1)

try:
    from MultipleAnalyzer.multiple_analyzer import MultipleModel
except Exception as e:
    print(f"Failed to import MultipleModel, error {e}.")
    sys.exit(1)

app = Flask(__name__)

# default model to use onload
g_dcf_default = True

@app.route("/", methods=["GET", "POST"])
def return_index():
    # initial render of html
    return render_template("stock_analyzer.html")

@app.route("/acceptForm", methods=["POST"])
def handle_form_accept():
    reply_message = {}
    error = None
    if request.method == "POST":
        if g_dcf_default:
            # run the dcf model
            if request.form.get("ticker") and request.form.get("rate"):
                ticker = request.form.get("ticker")
                rate = request.form.get("rate")
                try:
                    rate = float(rate)
                except ValueError:
                    error = e
                try:
                    reply_message = DCFModel(ticker, rate).run_model()
                except Exception as e:
                    error = e
                else:
                    reply_message["model"] = "dcf"
            else:
                error = "Please fill in all required fields."
        else:
            # run the multiples model
            if request.form.get("ticker"):
                ticker = request.form.get("ticker")
                try:
                    reply_message = MultipleModel(ticker).run_model()
                except Exception as e:
                    error = e
                else:
                    reply_message["model"] = "multiple"
            else:
                error = "Please fill in all required fields."

    if error is not None:
        reply_message = {"error": error}

    try:
        reply_message = jsonify(reply_message)
    except IndexError:
        print("Failed to convert reply message to JSON.")
    else:
        return reply_message
    

@app.route("/handle_model_change", methods=["POST"])
def handle_model_change():
    global g_dcf_default
    reply_message = {}
    error = None
    selected_button = request.form.get("selected_button")

    if selected_button == "dcf":
        g_dcf_default = True
    elif selected_button == "multiple":
        g_dcf_default = False
    else:
        error = "failed to set selected model"
    
    if error:
        reply_message = {"error": error}

    try:
        reply_message = jsonify(reply_message)
    except IndexError:
        print("Failed to convert reply message to JSON.")
    else:
        return reply_message


def main():
    parser = argparse.ArgumentParser(description="Stock Analyzer Web App")

    parser.add_argument(
        "-p", "--port",
        type=str,
        help="TCP port to host server on"
    )

    args = parser.parse_args()

    if args.port:
        port = args.port
    else:
        # use defualt port 8080
        port = "8080"

    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
