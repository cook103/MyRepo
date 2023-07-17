#!/usr/bin/env python3

from flask import Flask, render_template, json
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """Onload data is sent here"""
    return render_template("tic-tac-toe.html", onload_data=onload_data)

@app.route("/ReccuringData", methods=["GET", "POST"])
def return_scraped_data():
    """Reccuring data is sent here"""
    #return json.dumps(data)
    pass


def main():
    app.run(debug=True, port="8080")


if __name__ == "__main__":
    main()

# end
