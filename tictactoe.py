"""
Tic Tac Toe Player
"""

import math
import random

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
    return [[X, EMPTY, O],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


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

# Transition model
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

    # ==== RECURSIVE Functions ====
    
    def max_value_fn(board):
        # Base case
        if terminal(board):
            return utility(board)
        
        # Init value to minus infinity (so that first check ensure recursive process is happening)
        v = -math.inf

        # Recursive process
        for action in actions(board):
            resulting_board = result(board, action)
            v = max(v, min_value_fn(resulting_board))
        return v

    def min_value_fn(board):
        # Base case
        if terminal(board):
            return utility(board)
        
        # Init value to infinity
        v = math.inf

        for action in actions(board):
            resulting_board = result(board, action)
            v = min(v, max_value_fn(resulting_board))
        return v       
    
    # ====================================


    # HELPER + A/B PRUNING Function ======
    
    def best_action(board, minimax, target):

        # Get list of all possible actions
        all_possible_actions = actions(board)

        # If game just started, return any action
        if len(all_possible_actions) == 9:
            random_number = random.randint(0, 8)
            random_action = all_possible_actions[random_number]
            return random_action

        # Create var for storing list of [(action, score)]
        store_scores = []

        # Loop through actions
        for action in all_possible_actions:
            # Get score using either min_value_fn() if player is MAX
            # OR max_value_fn() if player is MIN
            resulting_state = result(board, action)
            score = minimax(resulting_state)
            # Target is 1 for MAX and -1 for min player
            if score == target:
                return action
            else:
                store_scores.append((action, score))
        
        # Return the first action whose score is 0.
        for action, score in store_scores:
            if score == 0:
                return action
            
    # ====================================

                
    # Get computer player
    computer_player = player(board)

    # If computer is "X", it's the MAX player (who wants to MAXIMISE score)
    if computer_player == X:
        return best_action(board, min_value_fn, 1)
    
    # If computer is "O", it's the MIN player (who wants to MINIMISE score)
    else:
        return best_action(board, max_value_fn, -1)

  

if __name__ == "__main__":
    board = initial_state()
    computer_player = player(board)
    # print()
    # print("GAME BEGINS")
    # print("-------------")
    # print()
    # print("BOARD")
    # for row in board:
    #     print(row)
    # print()
    minimaxgame = minimax(board)
