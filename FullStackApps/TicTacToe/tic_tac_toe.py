#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__)

# update the matrix based on POST requests recived
g_matrix = [
    "_", "_", "_",
    "_", "_", "_",
    "_", "_", "_",
]


@app.route("/", methods=["GET", "POST"])
def index():
    """Host the html page on index"""
    return render_template("tic_tac_toe.html")


@app.route("/recieve_square", methods=["POST"])
def recieve_square():
    """ "Recieve the X's spot from the user and
    return the best O's play"""
    if request.method == "POST":
        # X response from client
        data = (request.get_json())["button"]

        random_num = 2
        # return number to fill here

        x = {"o": random_num}  # test example
        return jsonify(x)


def find_best_move(board):
    empty_list = empty_spaces(board)
    print(empty_list)
    print(g_matrix)
    response["o"] = random.choice(empty_list)


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
