#!/usr/bin/env python3
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """Onload data is sent here"""
    return render_template("tic_tac_toe.html")

def main():
    app.run(debug=True, port="8080")


if __name__ == "__main__":
    main()

# end
