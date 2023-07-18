#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

matrix_clicked = {"num": ""}

@app.route("/", methods=["GET", "POST"])
def index():
    """Onload data is sent here"""
    onload_data = "hello"
    return render_template("tic_tac_toe.html", onload_data=onload_data)


@app.route("/recieve_square", methods=["POST"])
def recieve_square():
    data = request.get_json()
    matrix_clicked["num"] = data["button"]
    if (matrix_clicked["num"]) == "3":
        print("success")
        
    return data["button"]

def main(): 
    app.run(debug=True, port="8080")
    analyze_move()
    

if __name__ == "__main__":
    main()

# end
