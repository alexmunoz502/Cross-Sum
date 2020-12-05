import random
import copy

class Cell():
    def __init__(self, locked):
        self.locked = locked
        self.value = None
        self.down = None
        self.across = None

    def __repr__(self):
        if self.locked:
            return "X"
        else:
            return str(self.value)

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
                    
                    available_numbers = set()
                    available_numbers = available_numbers.union(get_available_numbers_by_row(grid, (i, j)))
                    available_numbers = available_numbers.intersection(get_available_numbers_by_column(grid, (i, j)))
                    
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

def print_grid(grid):
    for i in range(len(grid)):
        print(grid[i])            

def get_available_numbers_by_row(grid, position):
    """
    Returns the available numbers by row for an empty cell for puzzle generation
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

def get_available_numbers_by_column(grid, position):
    """
    Returns the available numbers by column for an empty cell for puzzle generation
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

def check_solution(grid) -> bool:
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
                if current_cell.across:
                    row_sum = get_across_sum(grid, i, j+1)
                    if current_cell.across != row_sum:
                        return False
                if current_cell.down:
                    col_sum = get_down_sum(grid, i + 1, j)
                    if current_cell.down != col_sum:
                        return False
    return True