#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__)


response = {"o": ""}

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
    button = data.get("button", None)
    if button is not None and len(button) == 1:
        g_matrix[int(button)] = "X" #temporary test case
        response["o"] = (find_best_move(g_matrix))
        return jsonify(response)
    else:
        raise ValueError("Incorrect Value Occured")

def get_square():
    """Hand off the O's spot to the user"""
    if response["o"] != "":
        print(response["o"])
        return jsonify(response)
    else:
        return "failed"

def find_best_move(board):
    empty_list = empty_spaces(board)
    print(empty_list)
    print(g_matrix)
    response["o"] = (random.choice(empty_list))


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
