"""
Tic Tac Toe Player
"""

import math

# Posible moves
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # return [[EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY]]

    return [[O, X, O],
            [X, X, O],
            [X, O, X]]


def player(board):
    """
    Returns the player who has the next turn on a board.
    """
    # If the board is empty, return X
    if all(cell is None for row in board for cell in row):
        return X

    # Count occurrences of X and O
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # The next player is X if X's count is not greater than O's
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Initialise a terminal state
    terminal_state = False

    # If no moves left, return True
    if board_full(board):
        terminal_state = True

    return terminal_state

def board_full(board):
    """
    Returns True if board does not have any "EMPTY" spots
    """
    empty_count = sum(row.count(EMPTY) for row in board)
    return not bool(empty_count)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


if __name__ == "__main__":
    board = initial_state()
    current_player = player(board)
    print("Current player is: ", current_player)
    print("Game is terminal: ", terminal(board))
