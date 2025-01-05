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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    # return [[EMPTY,         EMPTY,      EMPTY],
    #         [EMPTY,         EMPTY,      EMPTY],
    #         [EMPTY,         EMPTY,      EMPTY]]

    # return [[O,             O,          X],
    #         [X,             O,          EMPTY],
    #         [O,             X,          X]]


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
    if terminal(board):
        return None
    
    actions = set()
    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((row_index, cell_index))
    
    return sorted(actions)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    mark_board = player(board)

    if action not in actions(board):
        raise ValueError(f"Invalid move: {action} is not in available actions.")
    
    board_deep_copy = list(map(list, board))
    # board_deep_copy = [row[:] for row in board]
    # board_deep_copy = copy.deepcopy(board)

    row, cell = action
    board_deep_copy[row][cell] = mark_board

    return board_deep_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Initialize winner variable
    winner = None

    # Check rows for all X or O
    for row in board:
        if len(set(row)) == 1 and row[0] in [X, O]:
            winner = row[0]
            return winner
        
    # Check columns for all X or O
    for col in range(len(board[0])):
        column = [board[row][col] for row in range(len(board))]
        if len(set(column)) == 1 and column[0] in [X, O]:
            winner = column[0]
            return winner

    # Check main diagonal (0,0), (1,1), (2,2)
    main_diagonal = [board[i][i] for i in range(len(board))]
    if len(set(main_diagonal)) == 1 and main_diagonal[0] in [X, O]:
        winner = main_diagonal[0]
        return winner
    
    # Check anti diagonal (0,2), (1,1), (2,0)
    anti_diagonal = [board[i][len(board)-1-i] for i in range(len(board))]
    if len(set(anti_diagonal)) == 1 and anti_diagonal[0] in [X, O]:
        winner = anti_diagonal[0]
        return winner
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Initialise a terminal state
    terminal_state = False

    # If no moves left, return True
    if board_full(board) or winner(board):
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
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


if __name__ == "__main__":
    board = initial_state()
    current_player = player(board)
    # print("Game is terminal: ", terminal(board))
    print()
    print("=======")
    print("Current player is: ", current_player)
    print("Current Board:")
    print(board)
    print()
    print("Available spots: ")
    for action in actions(board):
        print(action)
    print()
    print("Result from action: ")
    print(result(board, (1,2)))
    new_board = result(board, (1,2))
    print(winner(new_board))
    print(terminal(new_board))
    print(utility(new_board))
    print("=======")
