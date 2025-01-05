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
    TBC

<br>


## `tictactoe.py`

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