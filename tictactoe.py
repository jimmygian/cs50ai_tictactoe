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

    # return [[X, X, O],
    #         [EMPTY, O, EMPTY],
    #         [EMPTY, EMPTY, EMPTY]]


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
    print()
    print("===============")
    print("===============")
    print()
    print("Current game board:")
    for row in board:
        print(row)
    print()    


    """ What's happening in MINIMAX algorithm?
    Given a state s, depending on whose turn is:
    - MAX picks action a in ACTIONS(s) that produces highest value of MIN-VALUE(RESULT(s, a))
    - MIN picks action a in ACTIONS(s) that produces smallest value of MAX-VALUE(RESULT(s, a))

    Explanation of MIN-VALUE(RESULT(s, a))
    - RESULT(s, a): What state results after I take this action?
    - MIN-VALUE(result): What happens when that MIN player tres to minimise the value of that state

    I need to consider that for ALL of possible actions, and after that, I need to pick the option that
    has the highest value.

    Explanation of MAX-VALUE(RESULT(s, a))

    """
    # Recursive algorithm - we need to repeat the exact same process, considering the opposite perspective

    def max_value_fn(board):      
        if terminal(board):
            return utility(board)
        
        # Init value to minus infinity (so that first check ensure recursive process is happening)
        v = -math.inf

        for action in actions(board):
            v = max(v, min_value_fn(result(board, action)))
        return v

    def min_value_fn(board):
        if terminal(board):
            return utility(board)
        
        # Init value to infinity
        v = math.inf

        for action in actions(board):
            v = min(v, max_value_fn(result(board, action)))
        return v       

    # Who's turn is it?
    computer_player = player(board)
    print("Computer player is: ", computer_player)

    
    if computer_player == X:
        # Check results of all possible scores and return action with max score
        store_scores = []

        for action in actions(board):
            score = min_value_fn(result(board, action))
            store_scores.append((action, score))

        print(store_scores)
       
        # Find the action with score -1, if it exists
        for act, score in store_scores:
            if score == 1:
                print("Best computer move: ", act)
                return act
        for act, score in store_scores:
            if score == 0:
                print("Best computer move: ", act)
                return act
    else:
        # Check results of all possible scores and return action with min score
        store_scores = []

        for action in actions(board):
            score = max_value_fn(result(board, action))
            store_scores.append((action, score))

        print(store_scores)

        # Find the action with score -1, if it exists
        for act, score in store_scores:
            if score == -1:
                print("Best computer move: ", act)
                return act
        for act, score in store_scores:
            if score == 0:
                print("Best computer move: ", act)
                return act


  

if __name__ == "__main__":
    board = initial_state()
    computer_player = player(board)
    # print("Game is terminal: ", terminal(board))
    print()
    print("GAME BEGINS")
    print("-------------")
    minimaxgame = minimax(board)
    print()
    print("NEXT ACTION: ", minimaxgame)
    print("-------------")

