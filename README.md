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

`runner.py` was already written. My assignment was to implement all the functions in `tictactoe.py`.


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

The minimax function calculates the best possible move for the player (`player(board)`) that plays next on the board and returns that move. 

The function is based on the MiniMax algorithm, which is a type of algorithm in adversarial search. Minimax represents winning conditions as (-1) for one side (the "MIN" side) and (+1) for the other side (the "MAX side). If we imagine that 0 is the middle where it's a tie, the minimizing side is trying to get the lowest score to win, while the maximizer is trying to get the highest score by the time the game ends.

For tic-tac-toe, we can imagine a terminal state where no one wins (0), a terminal state in which X wins (+1) and a terminal state in which O wins (-1). This means that X will be our MAX player that is trying to Maximize the score, and O will be our MIN player.

To better understand what we need to achive, let's think what we would do if we were playing the game and it was out turn. We would ask ourselves "If I take this action (e.g. put X in this position), what would my opponent do next?".  We could even try to visualize what we would do after our opponent's move, and what they would do after it, and so on, until the game reach the end and someone wins. Based on this train of thought, we would then choose the option that is the least favourable for our opponent. Of course, it's impossible for the human mind to do that so quickly, we can only think of few possible steps ahead.

For the computer on the other hand it's really easy - at least for tic-tac-toe that only has a few thousand moves in total. It can do this process and find each terminating state (if each player played optimally) for each available move. And that's what the minimax does, it checks for each move what would the terminating state and based on the result, it then returns the best choice.


To put it in pseudocode, the Minimax algorithm in this project works the following way:
* It first identifies which player is using the minimax algorithm (a.k.a is the computer). Since we have the option to choose which player we (the human) want to be, computer could be wither O or X.

* For each action of ACTIONS(_s_):
    - If computer player is X - a.k.a the MAX player, it picks the action _a_ in available ACTIONS(_s_) that produces the **HIGHEST value of MIN-VALUE(Result(_s, a_))**.
    - If computer player is O - a.k.a the MIN player, it picks the action _a_ in Actions(_s_) that produces **the LOWEST value of MAX-VALUE(Result(_s, a_))**.

