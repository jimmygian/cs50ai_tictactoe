# CS50AI | Lecture 0 - Search | Project 2 - `Tic-Tac-Toe`

This project is a mandatory assignment from **CS50AI – Lecture 0: "Search"**.

### 📌 Usage

To run the project locally, follow these steps:

1. **Clone the repository** to your local machine.

2. **Navigate to the project directory**:

   ```sh
   cd path/to/degrees
   ```

3. Install the libraries from the requirements.txt file

4. **Run the script in the terminal**
   Run `python runner.py` and enjoy.

<br>



## `tictactoe.py`

`runner.py` has already been written, and my task was to implement all the functions in `tictactoe.py`. While Alpha/Beta Pruning could be added at a later stage, it is not implemented at this time.


### `player(board)` Implementation

This function checks the current board's state and counts the empty, X, and O's. If all is empty, it returns "X". If X is equal or more than O, it returns O, else, it returns X. If the empty_count is 0, it does not matter what value it returns since the game is already over.

This function is using some pythonic expressions:

```Python
x_count = sum(row.count(X) for row in board)
o_count = sum(row.count(O) for row in board)
```

Step-by-step breakdown:

1. `row.count(X)`: Counts how many times X appears in a single row (list).

2. `for row in board`: Loops through each row in `board`.

3. `sum(...)`: Adds up the counts from all rows.

**Example Board**

```Python
board = [
    [X, O, X],
    [O, X, None],
    [X, None, O]
]
```

- board[0].count(X) = 2
- board[1].count(X) = 1
- board[2].count(X) = 1
- sum([2, 1, 1]) = 4

  So, `x_count = 4`. This method is concise, readable, and efficient compared to manually looping and counting.

<br>

Another expression used in this function is:

```Python
return X if x_count <= o_count else O
```

This is a ternary (conditional) expression in Python, which is a shorthand way to write an if-else statement in a single line.

Equivalent Long-form `if-else` Statement would be:

```Python
if x_count <= o_count:
    return X
else:
    return O

```

An alternative way of writing the above would be:

```Python
    # If not empty, count X, O and EMPTYs.
    x_count = 0
    o_count = 0
    empty_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
            else:
                empty_count += 1

    if empty_count == 0:
        return None
    elif x_count <= o_count:
        return X
    elif x_count > o_count:
        return O
```

### `result(board, action)` Implementation

The `result()` function returns a new board that reflects the state after making a move (represented by the `action`) on the current `board`. The `action` is a tuple `(i, j)`, where `i` is the row index and `j` is the column index. The function modifies the board based on the current player's move, which is determined by the `player(board)` function.

Here is the breakdown of the function:

1. **Check for valid action**:  
   The function first checks if the provided `action` is a valid move. This is done by verifying whether the action exists in the list of available actions returned by the `actions(board)` function.

    ```Python
    if action not in actions(board):
        raise ValueError(f"Invalid move: {action} is not in available actions.")
    ```

2. **Create a deep copy of the board**:

To ensure that the original board is not modified, a deep copy of the board is created. This prevents any side effects when changing the new board. This can be done using copy.deepcopy() or list comprehension.

There are multiple ways of implementing this, some more pythonic than others.

#### 1. Using `map()`

```Python
board_deep_copy = list(map(list, board))
```

The expression `list(map(list, board))` works as follows:

The `map()` function takes two arguments:
- a function to apply (`list` in this case).
- an iterable (here, board, which is a list of lists).

What `map(list, board)` does is apply the `list()` function to each element of board (which are lists themselves). The result is an iterator where each element (row) is converted into a new list. However, `map()` by itself returns an iterator, not a list.

Example:

```Python
board = [[1, 2, 3], [4, 5, 6]]
```

`map(list, board)` creates an iterator where each row is converted to a new list:

```Python
map(list, board)  # Result: <map object at 0x...> (an iterator)
```

The `list()` function converts the iterator returned by `map()` into a list. So, the `list(map(list, board))` call turns the result of `map()` into a new list. 

```Python
list(map(list, [[1, 2, 3], [4, 5, 6]]))  # Result: [[1, 2, 3], [4, 5, 6]]
```

#### 2. Using List Comprehension

```Python
board_deep_copy = [row[:] for row in board]
```

In this method, we use list comprehension to create a new list where each row from the board is copied. The slice `row[:]` creates a new list that contains **all the elements** of row. This ensures that each row is copied, and changes to the board_deep_copy will not affect the original board.

Explanation:
- `row[:]` creates a copy of row instead of just referencing the original list.
- `[row[:] for row in board]` iterates over each row in board, creating a new copy of each row and constructing a new list of lists (deep copy).

Example:

```Python
board = [[1, 2, 3], [4, 5, 6]]
board_deep_copy = [row[:] for row in board]
```
`board_deep_copy` will be a new list with the same content but independent of the original board.

#### 3. Using `copy.deepcopy()`

```Python
import copy

board_deep_copy = copy.deepcopy(board)
```

The `copy.deepcopy()` function from the `copy` module is a **built-in** way to create a deep copy of an object. It handles complex objects like lists of lists or nested data structures and ensures that all nested elements are copied, rather than just creating references to the original ones.

`copy.deepcopy()` works with more than just lists. It can handle a wide range of Python objects, including Tuples, sets, and custom objects.

Example
```Python
import copy

original_dict = {"key1": {"nested_key": 1}, "key2": 2}
copied_dict = copy.deepcopy(original_dict)
```


### `minimax(board)` Implementation

The `minimax` function calculates the **optimal move** for the next player in a tic-tac-toe game by simulating all possible moves and outcomes. It uses the **Minimax algorithm**, a recursive decision-making technique often used in two-player games like tic-tac-toe, chess, and checkers. Here's how the function works step by step:

---

#### **Core Idea of Minimax**
The algorithm assumes:
- **X (the MAX player)** tries to maximize the score (+1) by making the best possible move.
- **O (the MIN player)** tries to minimize the score (-1) by making the best possible move.
- A tie is neutral (score = 0).

The function explores all possible game states and selects the move that leads to the **best guaranteed outcome** for the current player, assuming both players play optimally.

---

#### **Key Components of the Function**

##### 1. **Recursive Helper Functions**
The function uses two recursive helpers: `max_value_fn` and `min_value_fn`.

- **`max_value_fn(board)`**:  
  Represents the MAX player's turn (player X).  
  - If the game is over (`terminal(board)`), it returns the game's score using `utility(board)`.
  - Otherwise, it recursively computes the maximum value of the possible moves by:
    1. Generating all available moves (`actions(board)`).
    2. Applying each move to the board (`result(board, action)`).
    3. Recursively calling `min_value_fn` to evaluate the resulting state.

- **`min_value_fn(board)`**:  
  Represents the MIN player's turn (player O).  
  - Similarly, if the game is over, it returns the score.
  - Otherwise, it computes the minimum value of the possible moves by:
    1. Generating all available moves.
    2. Applying each move to the board.
    3. Recursively calling `max_value_fn` to evaluate the resulting state.

These functions evaluate the entire game tree, ensuring the best decision is made for both players at every step.

---

##### 2. **Best Action Finder**
The `best_action` function selects the optimal move for the current player. Here's how it works:
- **For a starting board** (with no moves yet), it selects a random action since all moves are equally valid.
- For other cases:
  - It evaluates all possible actions.
  - If a move leads directly to a winning state (`score == target`, where `target` is +1 for MAX and -1 for MIN), it selects that move immediately.
  - Otherwise, it stores potential moves and selects the first neutral move (score = 0) if no winning move exists.

---

##### 3. **Player Identification**
The `player(board)` function determines the next player:
- If it's X's turn, `min_value_fn` is used to evaluate moves (because O will respond).
- If it's O's turn, `max_value_fn` is used to evaluate moves.


**Why This Works**

The idea here is to simulate the behavior of the opponent. If it's X's turn (the MAX player), it is crucial to evaluate the worst-case response from O, which is why min_value_fn is called. This ensures that X chooses the move that maximizes its score, even when O plays optimally to minimize X's score. Similarly, when it's O's turn (the MIN player), max_value_fn is used to evaluate the worst-case response from X. This guarantees that O chooses the move that minimizes its score, even when X plays optimally to maximize its score.

This alternating evaluation ensures that both players account for their opponent's best possible counter-moves, resulting in an optimal decision-making process.


---

#### **Flow of the Algorithm**
1. **Check if the game is over**:  
   If the game is already in a terminal state (win, loss, or draw), return the result directly.

2. **Simulate all possible moves**:  
   For each available action, simulate the resulting board state.

3. **Evaluate game outcomes**:  
   Use `max_value_fn` and `min_value_fn` to evaluate the best and worst outcomes for the current player.

4. **Select the best move**:  
   Return the move that maximizes or minimizes the player's score, depending on whether they're MAX or MIN.

---

#### **Why This Works**
- The algorithm guarantees an optimal move by exploring all possible game states.
- Even if the opponent plays optimally, the chosen move will lead to the best possible outcome (win or draw).

---

#### **Alpha-Beta Pruning**
Alpha-beta pruning is not fully implemented here but could be added to improve efficiency by skipping unnecessary branches in the game tree. This is especially useful in games with a larger search space, like chess.

---

#### **Example**
If the board state is:
```
X | O |  
---------
X |   | O
---------
  |   |  
```

- The function evaluates all possible moves for both X and O.
- It recursively simulates the game until the end state and calculates the scores for each move.
- Based on the scores, it selects the best move for the current player.
