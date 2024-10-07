# John Conway's Game of Life


"""
John Conway's Game of Life is a type of cellular automaton. It is a zero-player game, meaning that its evolution is
determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an
initial configuration and observing how it evolves.

The program defines its next "evolution" by the following rules:
1. Any live cell with fewer than two live neighbors dies, as if caused by underpopulation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

The way that we store our cells is in a 2D array. Each cell will have a value, either 1 or 0 (alive or dead). The
program will then iterate through each cell in the grid and apply the rules above to determine the next state of the
cell.

So, how do we check for neighbors? We can do this by checking the 8 cells surrounding the current cell. We can do this
using array indexing. In 2D arrays, we access a given cell with the syntax grid[row][col]. Where grid is the 2D array,
row is the row index, and col is the column index. We can then access the 8 surrounding cells by using the following
syntax:


    grid[row - 1][col - 1] | grid[row - 1][col] | grid[row - 1][col + 1]
    -----------------------|--------------------|-----------------------
    grid[row][col - 1]     | grid[row][col]     | grid[row][col + 1]
    -----------------------|--------------------|-----------------------
    grid[row + 1][col - 1] | grid[row + 1][col] | grid[row + 1][col + 1]


The center cell is grid[row][col], also known as the current cell. But there is a problem with this approach. What if
the current cell is on the edge of the grid? We would then be accessing cells that don't exist. To solve this,
we can use the modulo operator. The modulo operator returns the remainder of a division operation. We can use this to
wrap around the grid. For example, if we have a grid of size 10 x 10, and we are at index [0, 0], the neighbor
checking algorithm would attempt to access invalid values like [-1, -1] or [1, -1], to fix this we can use the modulo
operator to wrap around to the last index, 9 (remember that python starts indexing at 0 and the last one would be one
less than what we would normally use). We can do this by taking the index, modulo, the size of the grid. For example,
0 % 10 is 0, and 29 % 10 is 9. This allows us to wrap around the grid. So, our above format would look like this:

    grid[(row - 1) % N][(col - 1) % N] | grid[(row - 1) % N][col] | grid[(row - 1) % N][(col + 1) % N]
    -----------------------------------|--------------------------|-----------------------------------
    grid[row][(col - 1) % N]           | grid[row][col]           | grid[row][col + 1]
    -----------------------------------|--------------------------|-----------------------------------
    grid[(row + 1) % N][(col - 1) % N] | grid[(row + 1) % N][col] | grid[(row + 1) % N][(col + 1) % N]


Now, this takes a second to digest, but all that it is doing is taking the modulo of any index that has a modification
like (row - 1) or (col + 1) with "N", the size of the grid. This will allow us to wrap around the grid and avoid any
index out of bounds errors.

How do we implement this in code? We can create a function that will take the current grid and cell index.
The function will then return the number of live neighbors that the cell has. We can then use this function to apply
the rules of the game to each cell in the grid.
"""


def GetNeighbors(grid, row, col):
    N = len(grid)
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbors += grid[(row + i) % N][(col + j) % N]
    return neighbors


"""

Let's take a second to understand what this function is doing. We are taking the grid, row, and column as 
arguments. We then initialize a variable called neighbors to 0. We then iterate through the 8 surrounding cells using 
a nested loop. We then check if the current cell is the center cell. If it is, we skip it. We then add the value of 
the cell to the neighbors variable. We then return the number of neighbors that the cell has.

The "N = len(grid)" line is used to get the size of the grid. But, you may ask, what is the length of a 2D array? In 
python, the length function of a 2D array returns the number of rows. So, if we have a 10 x 10 grid, the length would 
be 10; if we had a 5 x 17 grid, the length would be 5. This is why we use the length of the grid to get the size of the
array, and, since it is a square grid, we can use the length of the grid to get the size of the width as well.

------------------------------------------------------------------------------------------------------------------------
If you wanted to get the dimensions of ANY 2D array, you would use the following code:
    rows = len(grid)
    cols = len(grid[0])
This works because grid[0] returns the first row of the 2D array, and the length of that row is the number of columns.
------------------------------------------------------------------------------------------------------------------------

The range() function in python takes the following parameters (arguments) range(start, stop, step). The range 
function returns a sequence of numbers, starting at "start" (0 by default), ending at "stop - 1" (No default since it 
is a required argument), and incrementing by "step" (1 by default) until it is larger than or equal to stop.

Ex. range(0, 10, 2) would return [0, 2, 4, 6, 8]
Ex. range(10) would return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

So, the nested loops are just a more compact way of writing out all the possible combinations of -1, 0, and 1.

The +=  operator is shorthand for adding the value on the right to the variable on the left. So, "a += b" is the same as
"a = a + b".

the return statement is used to return a value from a function, or in other words, the value that the function would 
"spit out". In this case, we are returning the number of neighbors



Since we have a function that can get the number of neighbors for a given cell, we can now apply the rules of the game
to each cell in the grid. We can do this by creating a new grid, applying the rules to each cell, and then setting the
new grid as the current grid. We can then repeat this process for a given number of iterations.

Let's create a function that will take the current grid and return the next state of the grid.
"""

import numpy as np


def NextState(grid):
    N = len(grid)
    new_grid = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            neighbors = GetNeighbors(grid, i, j)
            if grid[i][j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = 1
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1
    return new_grid


"""
Now, there is a lot more to digest here, but lets break it down from the start.

The "import numpy as np" line is used to import the numpy library and we give it the alias "np". Numpy is a powerful
library for working with arrays in python. It allows us to create multi-dimensional arrays, perform mathematical
operations on arrays, and much more. We use np.zeros() here to create the new grid of all zeros with dimensions
N x N.

*Later we will discuss the syntax of classes, methods, and why there are random periods and parameters in the code.*

Next, we iterate through each cell in the grid using two nested loops. We then get the number of neighbors for the 
current cell using the GetNeighbors() function. We then check if the current cell is alive (if grid[i][j] == 1:). If 
it is, we apply the rules of the game: If the cell has fewer than 2 neighbors or more than 3 neighbors (if neighbors < 2 or neighbors > 3:)
it dies. If it has 2 or 3 neighbors, it lives (else: new_grid[i][j] = 1). If the cell is dead, and it has exactly 3 
neighbors, it becomes alive (if neighbors == 3: new_grid[i][j] = 1). We then return the new grid.

Lets take a second to talk about the structure of if statements and conditionals. In python, an if statement is used to
execute a block of code if a condition is true. The syntax of an if statement is as follows:

    if condition:
        code to execute
        
But what if we have multiple conditions? We can use the "elif" keyword. The "elif" keyword is short for "else if". It
allows us to check multiple expressions for TRUE and execute a block of code as soon as one of the conditions is TRUE.
The syntax of an "elif" statement is as follows:

    if condition1:
        code to execute
    elif condition2:
        code to execute
    elif condition3:
        code to execute
    else:
        code to execute
        
The final else statement is used to execute code if none of the conditions are true. It is optional, and there can be at
most one else statement.

This can also be written as many conditions connected with logical operators. The logical operators in python are:
    
    and: Returns True if both statements are true
    or: Returns True if one of the statements is true
    not: Reverse the result, returns False if the result is true
    
for example:
    if condition1 and condition2:
        code to execute
        
    if condition1 or condition2:
        code to execute
        
    if not condition1:
        code to execute
        
Any combination of these operators can be used to create complex conditions.
        
A shorthand for not equal to is "!=". So, if we wanted to check if a variable "a" is not equal to 5, we would write:
    if a != 5:
        code to execute

instead of:
    if not(a == 5):
        code to execute
        

Another thing that sets python apart from other languages is the use of colons and indentation instead of curly 
braces. In python, the colon is used to denote the start of a block of code. The block of code is then indented. The 
indentation is used to group statements. The amount of indentation is up to the programmer, but it must be consistent 
throughout the block. The standard is to use 4 spaces for indentation (or the TAB key on keyboards). The end of the 
block is denoted by a line with less indentation or the end of the file.

For example, the if statement will not proceed to the elifs or else if it's condition is met. The same goes for the
elifs, if the condition is met, the else will not be executed. The else will only be executed if none of the conditions
are met. This is the same for loops, functions, and classes. The colon denotes the start of a block of code, and the
indentation groups the statements.

In other languages like C++, Java, and C#, curly braces are used to denote the start and end of a block of code. The
curly braces are required, and the indentation is optional. The curly braces are used to group statements. The end of
the block is denoted by a closing curly brace.

For example, the if statement in C++ would look like this:

    if (condition) {
        code to execute;
    }

But it can also be written like this and run exactly the same:
    
        if (condition)
        {
        code to execute;
        }

whereas in python, the second example would throw an error because of the indentation.


Now, moving back to the Game of Life, since we have a function that will take a grid of cells and return the next state
of the grid, we can now create a function to display our cells. We can do this by printing out the grid to the console.
Luckily, numpy formats its arrays in a nice way, so we can just print the array to the console.

If we wanted to display the grid in a more visual way, we could replace the 1's with a character like "X" and the 0's
with a character like ".". We can do this by iterating through each cell in the grid and replacing the values with the
appropriate character. We can then join the characters together to create a string for each row, and then join the rows
together to create the final grid. We can then print this grid to the console.

To print the array, it is very simple. We can just use the print() function and pass the array as an argument. The
print() function will then display the array to the console.



But what about an initial state? Its not very fun to start with a blank grid. We can create a function that will take
the size of the grid and return a random grid of cells. We can do this with numpy's random module. We can use the
np.random.choice() function to create a random grid of 1's and 0's. We can then return this grid.

The np.random.choice() function takes the following parameters:
    
    a: The array to choose from
    size: The shape of the output array
    p: The probabilities associated with each entry in a
 
 So, for us, we can use the following code to create a random grid of 1's and 0's:
     
        np.random.choice([0, 1], (N, N), p=[0.5, 0.5])
        
This will create a random grid of 1's and 0's with a 50% chance of each. We can then return this grid.
"""


def RandomGrid(N):
    return np.random.choice([0, 1], (N, N), p=[0.5, 0.5])


"""
Now lets put this all together! We will use a cool python feature called "if __name__ == '__main__':" to run our code.
This is used to check if the script is being run directly or being imported. If the script is being run directly, the
code inside the if statement will be executed. If the script is being imported, the code inside the if statement will
not be executed. This is useful for separating the code that should be run from the code that should be imported and
is a very tidy way to structure your code.


Lets start by importing the necessary libraries and defining the size of the grid.
"""



import numpy as np

import time # We will use this to slow down the output so that we can see the grid change
import os # We will use this to clear the console between each generation

N = 10


# Let's declare our functions which we created above.

def GetNeighbors(grid, row, col):
    N = len(grid)
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbors += grid[(row + i) % N][(col + j) % N]
    return neighbors


def NextState(grid):
    N = len(grid)
    new_grid = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            neighbors = GetNeighbors(grid, i, j)
            if grid[i][j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = 1
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1
    return new_grid


def RandomGrid(N):
    return np.random.choice([0, 1], (N, N), p=[0.5, 0.5])


# Now lets put it together in the if __name__ == '__main__': statement.


if __name__ == '__main__':
    # Create a random grid
    grid = RandomGrid(N)

    # Number of generations we want to do, in this case 10
    for i in range(10):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear') # Don't worry about this, it just clears the console
        
        # Print the grid
        print(grid)

        # Update the grid
        grid = NextState(grid)

        # Pause the output for 1 second
        time.sleep(1)

"""
Congratulations! You have now created a simple implementation of John Conway's Game of Life. You have learned how to
create a random grid of cells, get the number of neighbors for a given cell, apply the rules of the game to each cell,
and display the grid to the console. You have also learned about if statements, elif statements, else statements, the
modulo operator, the range() function, the numpy library, and the numpy.random.choice() function. You have also learned
about the if __name__ == '__main__': statement and how to clear the console in python.

For this demonstration, I have also created a visual representation of the grid. Since we are limited by the online 
IDE's and chromebooks

"""
