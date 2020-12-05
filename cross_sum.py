import random
import copy

# ====================================================================================================
# cross_sum.py
#
# This file contains the "backend" for the game. It contains the algorithms for generating and 
# solving the puzzles, as well as the functionality for checking solutions.
# =====================================================================================================


#region Class(es)
class Cell():
    """
    DECRIPTION
    Represents a cell in a grid for the game Cross Sum

    ATTRIBUTES
    locked : determines whether the cell is interactable or not. Locked cells are black, unlocked are white.
    value : the value assigned to the cell. Only used for white cells.
    down : the value representing the sum of the values of the white cells below (until another black cell is reached)
    across : the value representing the sum of the values of the white cells to the right (until another black cell is reached)
    """
    def __init__(self, locked : bool) -> None:
        """
        DESCRIPTION
        Initializes the Cell class

        PARAMETERS
        locked : sets the type of the cell, either locked or unlocked
        """
        self.locked = locked
        self.value = None
        self.down = None
        self.across = None
#endregion

#region Main Functions
def generate_puzzle(width : int, height : int) -> tuple:
    """
    DESCRIPTION
    Generates a new cross sum puzzle for the player to solve

    PARAMETERS
    width: The width of the game board grid (x-axis)
    height: The height of the game board grid (y-axis)

    RETURNS
    returns a tuple whose first element is the puzzle, and second element is the solution 
    """
    # Initialize grid
    grid = []
    grid_width = width
    grid_height = height

    # Generate an arbitrary number of black boxes using an arbitrary forumla
    black_boxes = 0
    black_boxes_limit = (((width - 2) * (height - 2)) * .25)

    # Algorithm to generate (and solve) the puzzle
    for i in range(height):
        # Add new row to board
        new_row = []
        grid.append(new_row)
        # Add columns to new row
        for j in range(width):
            new_col = None
            if ((i > 0 and j > 0)) and (i != height - 1 and j != width - 1):
                if (random.randint(1, 100) < 25 and black_boxes < black_boxes_limit):
                    new_col = Cell(locked=True)
                    black_boxes += 1
                else:
                    
                    available_numbers = get_available_numbers(grid, (i, j))
                    
                    if len(available_numbers) == 0:
                        new_col = Cell(locked=True)
                    else:
                        new_col = Cell(locked=False)
                        assigned_value = random.choice(tuple(available_numbers))
                        new_col.value = assigned_value
            else:
                new_col = Cell(locked=True)
            grid[i].append(new_col)

    # Populate Black Cell Down and Across Values
    for i in range(height):
        for j in range(width):
            current_cell = grid[i][j]
            # Top left and top left cells will always be blank black boxes
            if (i == 0 and j == 0) or (i == 0 and j == width - 1):
                pass
            # Fill in horizontal row headers
            if (j < width - 1) and (current_cell.locked) and not (grid[i][j + 1].locked):
                current_cell.across = get_across_sum(grid, i, j + 1)
            # Fill in vertical column headers
            if (i < height - 1) and (current_cell.locked) and not (grid[i + 1][j].locked):
                current_cell.down = get_down_sum(grid, i + 1, j)

    # Store completed puzzle as solution
    solution = copy.deepcopy(grid)

    # Erase values from white cells
    for row in grid:
        for col in row:
            if not col.locked:
                col.value = None

    return (grid, solution)

def check_solution(grid : list) -> bool:
    """
    DESCRIPTION
    Checks whether or not the current state of the board results in a completed puzzle

    RETURN
    returns true if the puzzle is complete, otherwise returns false
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            current_cell = grid[i][j]
            if current_cell.locked:
                # Decision Check: Sums of rows match their corresponding row/column headers
                if current_cell.across:
                    row_sum = get_across_sum(grid, i, j+1)
                    if current_cell.across != row_sum:
                        return False
                if current_cell.down:
                    col_sum = get_down_sum(grid, i + 1, j)
                    if current_cell.down != col_sum:
                        return False
            else:
                # Decision Check: White box value is an integer between 1 and 9
                if not (0 < current_cell.value < 10):
                    return False

                # Decision Check: No duplicate values 
                if check_has_duplicate_values(grid, (i, j)):
                    return False
    return True
#endregion

#region Helper Functions
def get_available_numbers(grid : list, position : tuple) -> set:
    """
    DESCRIPTION
    Returns a set of valid numbers that correspond to a cell in a grid

    PARAMETERS
    grid : the grid which contains the cell for which we are trying to find the available numbers for
    position : the position of the cell in the grid

    RETURN
    returns a set integers
    """
    available_numbers = set()
    available_numbers = available_numbers.union(get_available_numbers_by_row(grid, (position[0], position[1])))
    available_numbers = available_numbers.intersection(get_available_numbers_by_column(grid, (position[0], position[1])))
    return available_numbers

def get_available_numbers_by_row(grid : list, position : tuple) -> set:
    """
    DESCRIPTION
    A helper function of the get_available_numbers functions which finds all of the available numbers
    for a cell based on the row only

    PARAMETERS
    grid : the grid containing the cell
    position : the position of the cell in the grid

    RETURN
    Returns a set of integers
    """
    available_numbers = {number for number in range(1, 10)}
    if position[0] - 1 == 0:
        return available_numbers
    else:
        for i in range(position[0] - 1, 0, -1):
            if grid[i][position[1]].locked:
                break
            available_numbers.remove(grid[i][position[1]].value)
    return available_numbers

def get_available_numbers_by_column(grid : list, position : tuple) -> set:
    """
    DESCRIPTION
    A helper function of the get_available_numbers functions which finds all of the available numbers
    for a cell based on the column only

    PARAMETERS
    grid : the grid containing the cell
    position : the position of the cell in the grid

    RETURN
    Returns a set of integers
    """
    available_numbers = {number for number in range(1, 10)}
    if position[1] == 1:
        return available_numbers
    else:
        for i in range(position[1]-1, 0, -1):
            if grid[position[0]][i].locked:
                break
            available_numbers.remove(grid[position[0]][i].value)
    return available_numbers
    
def get_across_sum(grid, x : int, y : int) -> int:
    """
    DESCRIPTION
    A recursive function that, given cell at location (x,y), retreives the the sum of 
    all the white cells to the right until a black cell is reached.

    PARAMETERS
    x : the position of the cell on the x axis
    y : the position of the cell on the y axis

    RETURN
    returns the sum of the cells
    """
    try:
        current_cell = grid[x][y]
        if not current_cell.locked:
            return current_cell.value + get_across_sum(grid, x, y + 1)
        else:
            return 0
    except (IndexError):
        return 0

def get_down_sum(grid, x : int, y : int) -> int:
    """
    DESCRIPTION
    A recursive function that, given cell at location (x,y), retreives the the sum of 
    all the white cells to below until a black cell is reached.

    PARAMETERS
    x : the position of the cell on the x axis
    y : the position of the cell on the y axis

    RETURN
    returns the sum of the cells
    """
    try:
        current_cell = grid[x][y]
        if not current_cell.locked:
            return (current_cell.value if current_cell.value else 0) + get_down_sum(grid, x + 1, y)
        else:
            return 0
    except (IndexError):
        return 0

def check_has_duplicate_values(grid : list, position : tuple) -> bool:
    """
    DESCRIPTION
    given a cell in a grid, this function checks if the value of the cell is unique
    within it's entire row and column

    PARAMETERS
    grid : the grid where the cell is in
    position : the position of the cell in the grid

    RETURN
    returns true if there are duplicate values in the row or column, otherwise returns false
    """
    value = grid[position[0]][position[1]]
    # Check Cells Above
    for i in range(position[0], 0):
        current_cell = grid[i][position[1]]
        if current_cell.locked:
            break
        if current_cell.value == value:
                return True
    # Check Cells Below
    for i in range(position[0], len(grid)):
        current_cell = grid[i][position[1]]
        if current_cell.locked:
            break
        if current_cell.value == value:
            return True

    # Check Cells Left
    for i in range(position[1], 0):
        current_cell = grid[position[0]][i]
        if current_cell.locked:
            break
        if current_cell.value == value:
            return True

    # Check Cells Right
    for i in range(position[1], len(grid[position[0]])):
        current_cell = grid[position[0]][i]
        if current_cell.locked:
            break
        if current_cell.value == value:
            return True

    return False
#endregion

