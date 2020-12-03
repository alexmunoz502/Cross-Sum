import random
import copy

class NonEditableCell(Exception):
    """
    DESCRIPTION
    An error that is thrown when the value of a locked cell is attempted to be changed
    """
    pass


class WhiteCell():
    def __init__(self):
        self._value = None

    def __repr__(self):
        return f"_{self.value if self.value is not None else '_'}_"
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class BlackCell():
    def __init__(self):
        self._down_value = None
        self._across_value = None

    def __repr__(self):
        return f"{self.down_value if self.down_value is not None else 'X'}\\{self.across_value if self.across_value is not None else 'X'}"

    @property
    def down_value(self):
        return self._down_value

    @down_value.setter
    def down_value(self, new_value):
        self._down_value = new_value

    @property
    def across_value(self):
        return self._across_value

    @across_value.setter
    def across_value(self, new_value):
        self._across_value = new_value
        

class CrossSum():
    """
    DESCRIPTION
    Represents a session of Cross Sum
    """
    def __init__(self) -> None:
        """
        DESCRIPTION
        Initializes the game session
        """
        self.board = None
        self.width = None
        self.height = None
        self.solution = None

    def generate_puzzle(self, width : int, height : int) -> None:
        """
        DESCRIPTION
        Generates a new cross sum puzzle for the player to solve

        PARAMETERS
        width: The width of the game board grid (x-axis)
        height: The height of the game board grid (y-axis)
        """
        self.board = []
        self.width = width
        self.height = height
        black_boxes = 0
        black_boxes_limit = (((width - 2) * (height - 2)) * .25) // 1 # Arbirary formula to come up with number of black boxes in puzzle
        for i in range(width):
            # Add new row to board
            new_row = []
            self.board.append(new_row)
            # Add columns to new row
            for j in range(height):
                new_col = None
                if ((i > 0 and j > 0)) and (i != width - 1 and j != height - 1):
                    if (random.randint(1, 100) < 25 and black_boxes < black_boxes_limit):
                        new_col = BlackCell()
                        black_boxes += 1
                    else:
                        new_col = WhiteCell()
                        new_col.value = random.randint(1, 9)
                else:
                    new_col = BlackCell()
                self.board[i].append(new_col)

        for i in range(width):
            for j in range(height):
                current_cell = self.board[i][j]
                # Top left and top left cells will always be blank black boxes
                if (i == 0 and j == 0) or (i == 0 and j == height-1):
                    pass
                # Fill in horizontal row headers
                if (j < height - 1) and (type(current_cell) == BlackCell) and (type(self.board[i][j + 1]) == WhiteCell):
                    current_cell.across_value = self.get_across_sum(i, j + 1)
                # Fill in vertical column headers
                if (i < width - 1) and (type(current_cell) == BlackCell) and (type(self.board[i + 1][j]) == WhiteCell):
                    current_cell.down_value = self.get_down_sum(i + 1, j)
                else:
                    pass

        # Store completed puzzle as possible solution
        self.solution = copy.deepcopy(self.board)

        # # Erase values from white cells
        for row in self.board:
            for col in row:
                if type(col) == WhiteCell:
                    col.value = None
                
    def get_across_sum(self, x : int, y : int) -> int:
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
            current_cell = self.board[x][y]
            if type(current_cell) == WhiteCell:
                return current_cell.value + self.get_across_sum(x, y + 1)
            else:
                return 0
        except (IndexError):
            return 0

    def get_down_sum(self, x : int, y : int) -> int:
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
            current_cell = self.board[x][y]
            if type(current_cell) == WhiteCell:
                return (current_cell.value if current_cell.value else 0) + self.get_down_sum(x + 1, y)
            else:
                return 0
        except (IndexError):
            return 0

    def check_solution(self) -> bool:
        """
        DESCRIPTION
        Checks whether or not the current state of the board results in a completed puzzle

        RETURN
        returns true if the puzzle is complete, otherwise returns false
        """
        for i in range(self.width):
            for j in range(self.height):
                current_cell = self.board[i][j]
                if type(current_cell) == BlackCell:
                    if current_cell.across_value:
                        row_sum = self.get_across_sum(i, j+1)
                        if current_cell.across_value != row_sum:
                            return False
                    if current_cell.down_value:
                        col_sum = self.get_down_sum(i + 1, j)
                        if current_cell.down_value != col_sum:
                            return False
        return True

    def print_board(self):
        for row in self.board:
            print(row)

    def make_move(self, x : int, y : int, new_value : int) -> bool:
        """
        DESCRIPTION
        Attempts to make a move by changing the value at position (x,y) to a new value.
        Only White cells can have their values changed

        PARAMETERS
        x : the position of the cell on the x axis
        y : the position of the cell on the y axis
        new_value : the value to update the cell's value to

        RETURN
        returns True if the move was successful, otherwise returns False
        """
        selected_cell = self.board[x][y]
        if type(selected_cell) == WhiteCell:
            selected_cell.value = new_value
            return True
        else:
            return False

    def game_loop(self):
        while True:
            # Prompt player for a puzzle size
            print("What size puzzle would you like to play?")
            rows = int(input("rows: "))
            columns = int(input("columns: "))
            # Generate a new puzzle to solve
            self.generate_puzzle(rows, columns)

            # Start Game Loop
            while True:
                # Display board to player
                self.print_board()

                # prompt input
                print("If you want to check for solution, enter nothing")
                move = input("Else to make a move (format 'row,col,value'): ")
                if move == "":
                    if self.check_solution():
                        print("You solved it!")
                        break
                    else:
                        print("The puzzle is not yet solved.")
                else:
                    move_array = move.split(",")
                    row = int(move_array[0])
                    col = int(move_array[1])
                    value = int(move_array[2])

                # make move
                self.make_move(row, col, value)

if __name__ == "__main__":
    #random.seed()
    cross_sum = CrossSum()
    cross_sum.generate_puzzle(4, 4)
    cross_sum.game_loop()
    #
    #cross_sum.make_move(1, 1, 8)
    #cross_sum.make_move(1, 2, )
    #
    print(f"{'You win!' if cross_sum.check_solution() else 'The puzzle is not yet complete.'}")