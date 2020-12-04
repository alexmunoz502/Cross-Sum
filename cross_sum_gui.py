# Import Dependencies
import pygame
import random
import copy

# Pygame Initialization
pygame.init()

# New Random Seed
random.seed()

# COLORS
WHITE = (245, 245, 246)
LIGHT = (220, 220, 221)
MEDIUM = (197, 195, 198)
DARK = (70, 73, 76)
ACCENT_1 = (76, 92, 104)
ACCENT_2 = (25, 133, 161)

# TEXT
SYSFONT = pygame.font.get_default_font()
TITLE_FONT = pygame.font.SysFont(SYSFONT, 50)
SUBTITLE_FONT = pygame.font.SysFont(SYSFONT, 30)
HEADER_FONT = pygame.font.SysFont(SYSFONT, 12)
TEXT_FONT = pygame.font.SysFont(SYSFONT, 16)

# CONSTANTS
CELL_WIDTH = 25
CELL_HEIGHT = 25
CELL_SPACE = 1

# Game Classes
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

# Drawing Surfaces
screen = pygame.display.set_mode([800, 600])
title_text = TITLE_FONT.render("Cross Sum", False, ACCENT_1)

# Screen Variables
screen_width, screen_height = pygame.display.get_surface().get_size()

def play():

    game = CrossSum()
    game.generate_puzzle(4, 16)

    running = True
    while running:
        # Close Window Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background Color
        screen.fill(WHITE)

        # Draw Title
        title_offset = (screen_width / 2) - (title_text.get_width() / 2)
        screen.blit(title_text, (title_offset, 25))

        # Draw Board
        board_pixel_width = (game.height * (CELL_WIDTH + CELL_SPACE))
        board_pixel_height = (game.width * (CELL_HEIGHT + CELL_SPACE))
        x_offset = (screen_width / 2) - (board_pixel_width / 2) 
        y_offset = (screen_height / 2) - (board_pixel_height / 2)
        draw_game_board(game, screen, x_offset, y_offset)
        
        # Flip the display
        pygame.display.flip()

def draw_game_board(game, surface, start_x, start_y):
    # Initialize Variables
    game_board = game.board
    board_width = game.width
    board_height = game.height

    x_offset = 0
    y_offset = 0

    # Draw Game Board
    for i in range(board_width):
        x_offset = 0
        for j in range(board_height):
            # Variables
            current_cell = game_board[i][j]

            # Set Colors
            cell_color = (DARK if type(current_cell) is BlackCell else LIGHT)
            text_color = (LIGHT if type(current_cell) is BlackCell else DARK)
            # Draw
            pygame.draw.rect(surface, cell_color, (start_x + x_offset, start_y + y_offset, CELL_WIDTH, CELL_HEIGHT))

            # Draw split in black cell
            if type(current_cell) is BlackCell:
                pygame.draw.line(surface, MEDIUM, (start_x + x_offset, start_y + y_offset), (start_x + x_offset + CELL_WIDTH, start_y + y_offset + CELL_HEIGHT))

            # Set Text
            text=""
            if (type(current_cell) is BlackCell):
                # Down Value
                down_text = str(current_cell.down_value) if current_cell.down_value is not None else ""
                text_surface = HEADER_FONT.render(down_text, False, text_color)
                screen.blit(text_surface, (start_x + x_offset + (CELL_WIDTH / 8), start_y + y_offset + (CELL_HEIGHT / 2)))
                # Across Value
                across_text = str(current_cell.across_value) if current_cell.across_value is not None else ""
                text_surface = HEADER_FONT.render(across_text, False, text_color)
                screen.blit(text_surface, (start_x + x_offset + (CELL_WIDTH / 2), start_y + y_offset + (CELL_HEIGHT / 8)))
            else:
                # Cell Value
                value_text = str(current_cell.value) if current_cell.value is not None else ""
                text_surface = TEXT_FONT.render(value_text, False, text_color)
                screen.blit(text_surface, (start_x + x_offset, start_y + y_offset))

            
            x_offset += CELL_WIDTH + CELL_SPACE
        y_offset += CELL_HEIGHT + CELL_SPACE

if __name__ == "__main__":
    play()
    pygame.quit()