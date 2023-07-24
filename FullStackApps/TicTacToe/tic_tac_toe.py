#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__)

X_PLAYER = "X"
O_PLAYER = "O"
EMPTY = "_"

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
        g_matrix[int(data)] = X_PLAYER

        random_num = find_best_move()
        x = {"o": random_num[0], "game_over": random_num[1], "board": g_matrix}  # test example
        print(x)
        return jsonify(x)



def score(board):
    # Checking Rows for X or O win
    for x in range (3):
        if board[x*3] == board[(x*3)+1] and board[(x*3)+1] == board[(x*3)+2]:
            if board[x*3] == X_PLAYER:
                return -10
            elif board[x*3] == O_PLAYER:
                return 10
    # Checking Columns for X or O win
    for x in range (3):
        if board[x] == board[x+3] and board[x+3] == board[x+6]:
            if board[x] == X_PLAYER:
                return -10
            elif board[x] == O_PLAYER:
                return 10
    #Checking Diagonals for X or O win
    if board[0] == board[4] and board[4] == board[8]:
        if board[0] == X_PLAYER:
            return -10
        elif board[0] == O_PLAYER:
            return 10
    if board[2] == board[4] and board[4] == board[6]:
        if board[2] == X_PLAYER:
            return -10
        elif board[2] == O_PLAYER:
            return 10
    return None


def minimax(board, depth, is_maxing):
    if score(board) is not None:
        return score(board)
    empty_list = empty_spaces(board)
    # Checking for a draw
    if len(empty_list) == 0:
        return 0
    if(is_maxing):
        best_val = -1000
        for space in empty_list:
            board[space] = O_PLAYER
            best_val = max(best_val, minimax(board, depth + 1, not is_maxing))
            board[space] = EMPTY
        return best_val

    else:
        best_val = 1000
        for space in empty_list:
            board[space] = X_PLAYER
            best_val = min(best_val, minimax(board, depth + 1, not is_maxing))
            board[space] = EMPTY
        return best_val

def find_best_move():
    best_val = -1000
    best_move = -1
    empty_list = empty_spaces(g_matrix)
    for space in empty_list:
        g_matrix[space] = O_PLAYER
        move_val = minimax(g_matrix, 9 - len(empty_list), False)
        g_matrix[space] = EMPTY
        if move_val > best_val:
            best_move = space
            best_val = move_val
    
    g_matrix[best_move] = O_PLAYER
    empty_list = empty_spaces(g_matrix)
    print(empty_list)
    print(g_matrix)
    game_over = False
    if(len(empty_list) == 0 or best_val == 10):
        game_over = True
    return (best_move, game_over)


def empty_spaces(board):
    empty_list = []
    i = 0
    for space in board:
        if space == EMPTY:
            empty_list.append(i)
        i += 1
    return empty_list


def main():
    app.run(debug=True, port="8080")


if __name__ == "__main__":
    main()

# end
