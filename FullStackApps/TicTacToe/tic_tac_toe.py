#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

g_matrix = [
     "", "", "",
     "", "", "",
     "", "", "",
]

matrix_clicked = {"num": ""}

@app.route("/", methods=["GET", "POST"])
def index():
    """Host the html page on index"""
    onload_data = "hello"
    return render_template("tic_tac_toe.html", onload_data=onload_data)


@app.route("/post_square", methods=["POST"])
def recieve_square():
    """"Recieve the X's spot from the user"""
    data = request.get_json()
    matrix_clicked["num"] = data["button"]
    
    if (matrix_clicked["num"]) == "3":
        print("success")

    return data["button"]

@app.route("/get_square", methods=["GET"])
def get_square(data):
    """Hand off the O's spot to the user"""
    
    get_data = {
        "matrix": data
    }

    return jsonify(get_data)

def find_best_move(board):
    empty = empty_spaces(board)
    return

def empty_spaces(board):
    empty = []
    i = 0
    for space in board:
        if space == "":
            empty.append(i)
        i += 1

def main(): 
    app.run(debug=True, port="8080")
    analyze_move()
    

if __name__ == "__main__":
    main()

# end
