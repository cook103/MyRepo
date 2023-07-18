#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

g_matrix = [
     "_", "_", "_",
     "_", "_", "_",
     "_", "_", "_",
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
    if matrix_clicked["num"] != str(0):
        g_matrix[0] = "X" #temporary test case
        find_best_move(g_matrix)
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
    empty_list = empty_spaces(board)
    print(empty_list)
    print(g_matrix)
    get_square(random.choice(empty_list))

def empty_spaces(board):
    empty_list = []
    i = 0
    for space in board:
        if space == "_":
            empty_list.append(i)
        i += 1
    return empty_list

def main(): 
    app.run(debug=True, port="8080")

if __name__ == "__main__":
    main()

# end
