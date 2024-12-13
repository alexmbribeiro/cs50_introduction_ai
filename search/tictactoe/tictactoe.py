"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # player "x" starts the game
    if (board == initial_state()):
        return X

    # count the amount of plays by each player
    count_x = 0
    count_o = 0
    for row in board:
        for column in row:
            if (column == X):
                count_x += 1
            elif (column == O):
                count_o += 1

    # if player "x" has played more times then player "o" it means it is player "o" turn. the opposite applies as well
    if (count_x > count_o):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # initialize the set
    possible_actions = set()

    # if a column is empty, then it is a possible action
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:  # Check if the cell is empty
                possible_actions.add((i, j))  # Add the (row, column) indices to the set

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # if the action is within bounds
    if not (0 <= action[0] <= 2 and 0 <= action[1] <= 2):
        raise ValueError("Action is out of bounds")

    # if the action is a tuple or has the correct structure
    if not isinstance(action, tuple) or len(action) != 2:
        raise TypeError("Action must be a tuple with two integers (i, j)")

    # if the specified position is already occupied
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Action is invalid: cell is already occupied")

    # deepcopy the board to not modify relevant data
    result_board = copy.deepcopy(board)

    # make the move
    result_board[action[0]][action[1]] = player(board)

    # return the new board
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for row
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    # Check for vertical
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] and board[0][column] != EMPTY:
            return board[0][column]

    # Check for diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    # If no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    for row in board:
        for column in row:
            if (column == EMPTY and winner(board) == None):
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    game_over = winner(board)

    if (game_over == X):
        return 1
    elif (game_over == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board)):
        return None

    if (player(board) == X):
        m = -9999999
        for action in actions(board):
            minimum_value = min_value(result(board, action))
            if (m < minimum_value):
                m = minimum_value
                action_to_take = action
    else:
        m = 9999999
        for action in actions(board):
            maximum_value = max_value(result(board, action))
            if (m > maximum_value):
                m = maximum_value
                action_to_take = action

    return action_to_take


def max_value(board):
    if (terminal(board)):
        return utility(board)

    m = -9999999
    for action in actions(board):
        m = max(m, min_value(result(board, action)))

    return m


def min_value(board):
    if (terminal(board)):
        return utility(board)

    m = 9999999
    for action in actions(board):
        m = min(m, max_value(result(board, action)))

    return m