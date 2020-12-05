import pygame
import sys
import cross_sum

# ====================================================================================================
# app.py
#
# This file contains the "frontend" for the game. It contains the code for the GUI, which is 
# responsible for displaying the information to the player and accepting input to play the game
# =====================================================================================================

pygame.init()

#region Application Settings / Constants
#region Window
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 500
#endregion

#region Fonts
SYSFONT = pygame.font.get_default_font()
TITLE_FONT = pygame.font.SysFont(SYSFONT, 50)
SUBTITLE_FONT = pygame.font.SysFont(SYSFONT, 25)
NUMBER_FONT = pygame.font.SysFont(SYSFONT, 24)
HEADER_FONT = pygame.font.SysFont(SYSFONT, 13)
BUTTON_FONT = pygame.font.SysFont(SYSFONT, 16)
#endregion

#region Colors
WHITE = (245, 245, 246)
LIGHT = (220, 220, 221)
MEDIUM = (197, 195, 198)
DARK = (70, 73, 76)
ACCENT_1 = (76, 92, 104)
ACCENT_2 = (25, 133, 161)
RED = (140, 94, 88)
GREEN = (92, 116, 87)
HIGHLIGHT = (255, 255, 117)
#endregion

#region Grid Cell Size
CELL_WIDTH = 25
CELL_HEIGHT = 25
CELL_NUMBER_X_OFFSET = 8
CELL_NUMBER_Y_OFFSET = 5
#endregion
#endregion

#region Classes
class Button():
    """
    DESCRIPTION
    an pygame implementation of a GUI button.
    """
    def __init__(self, x : int, y : int, width: int, height: int, text : str = None, function = None) -> None:
        """
        DESCRIPTION
        initializes the pygame button

        PARAMETERS
        x : the location on the x axis of the window
        y : the location on the y axis of the window
        width : the width in pixels of the button
        height : the height in pixels of the button
        text : the text to display on top of the button
        function: the function to call when the button is pressed
        """
        self.image = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.text = text
        self.function = function

        self.color = ACCENT_1
        self.hover_color = ACCENT_2
        self.text_color = WHITE

        self.hovered = False

    def update(self, mouse : tuple) -> None:
        """
        DESCRIPTION
        every update cycle of the game, the update method is called

        PARAMETERS
        mouse : the current position of the mouse's cursor
        """
        if self.rect.collidepoint(mouse):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, window) -> None:
        """
        DESCRIPTION
        every draw cycle of the game, this method is called

        PARAMETERS
        window : the window to draw the button on
        """
        self.image.fill(self.hover_color if self.hovered else self.color)
        window.blit(self.image, self.position)

        if (self.text):
            button_text = BUTTON_FONT.render(self.text, True, self.text_color)
            button_text_width = button_text.get_width()
            button_text_height = button_text.get_height()
            position_x = self.position[0] + (self.width - button_text_width) // 2
            position_y = self.position[1] + (self.height - button_text_height) // 2
            window.blit(button_text, (position_x, position_y))

    def action(self) -> None:
        """
        DESCRIPTION
        called when the button is clicked, this function calls the button's stored function
        """
        self.function()

class App():
    """
    DESCRIPTION
    The main application of the game. With support from the cross sum file, runs the game.
    """
    def __init__(self) -> None:
        """
        DESCRIPTION
        initializes the application
        """
        # Sys / App
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.mouse_position = None

        # Buttons
        self.buttons = []
        self.initialize_buttons()

        # Game / Grid
        self.selected = None
        self.difficulties = [(4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
        self.difficulty_names = ["4 x 4", "5 x 5", "6 x 6", "7 x 7", "8 x 8", "9 x 9"]
        self.difficulty = self.difficulty_names[2]
        self.grid_option = self.difficulties[2]
        self.initialize_grid()

        # Messaging
        self.banner = ""
        self.banner_color = WHITE

    def initialize_buttons(self) -> None:
        """
        DESCRIPTION
        initializes the buttons on the GUI
        """
        self.buttons.append(Button(75, 400, 50, 50, "New", self.initialize_grid))
        self.buttons.append(Button(75, 455, 10, 10, "-", self.decrease_difficulty))
        self.buttons.append(Button(115, 455, 10, 10, "+", self.increase_difficulty))
        self.buttons.append(Button(150, 400, 50, 50, "Check", self.check_solution))
        self.buttons.append(Button(225, 400, 50, 50, "Solve", self.auto_solve))

    def initialize_grid(self) -> None:
        """
        DESCRIPTION
        initializes a new cross sum puzzle for the user to play
        """
        # Clear Messages
        self.banner = ""
        self.banner_color = WHITE
        # Generate Puzzle
        self.grid_width = self.grid_option[0]
        self.grid_height = self.grid_option[1]
        self.grid, self.solution = cross_sum.generate_puzzle(self.grid_width, self.grid_height)
        self.grid_pixel_width = self.grid_width * (CELL_WIDTH)
        self.grid_pixel_height = self.grid_height * (CELL_HEIGHT)
        self.grid_x = (WINDOW_WIDTH / 2) - (self.grid_pixel_width / 2)
        self.grid_y = (WINDOW_HEIGHT / 2) - (self.grid_pixel_height / 2)

    def check_solution(self) -> None:
        """
        DESCRIPTION
        checks if the player has won the game and updates the banner to a corresponding message
        """
        is_solved = cross_sum.check_solution(self.grid)
        if (is_solved): 
            self.banner = "You solved the puzzle!"
            self.banner_color = GREEN
        else:
            self.banner = "The puzzle is not solved"
            self.banner_color = RED

    def auto_solve(self) -> None:
        """
        DESCRIPTION
        automatically solves the puzzle for the user
        """
        self.grid = self.solution

    def increase_difficulty(self) -> None:
        """
        DESCRIPTION
        increases the difficulty of the game when the player generates the next puzzle
        """
        option_index = self.difficulties.index(self.grid_option)
        if option_index == (len(self.difficulties) - 1):
            return
        else:
            self.grid_option = self.difficulties[option_index + 1]
            self.difficulty = self.difficulty_names[option_index + 1]

    def decrease_difficulty(self) -> None:
        """
        DESCRIPTION
        decreases the difficulty of the game when the player generates the next puzzle
        """
        option_index = self.difficulties.index(self.grid_option)
        if option_index == 0:
            return
        else:
            self.grid_option = self.difficulties[self.difficulties.index(self.grid_option) - 1]
            self.difficulty = self.difficulty_names[option_index - 1]

    def run(self) -> None:
        """
        DESCRIPTION
        main method for the application, runs the events, updates, and drawing for each step or "tick" of the game
        """
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def events(self) -> None:
        """
        DESCRIPTION
        event handling for user input
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_cell = self.get_mouseover_grid_cell()
                self.selected = clicked_cell if (self.selected != clicked_cell) else None

                for button in self.buttons:
                    if button.hovered:
                        button.action()

            if event.type == pygame.KEYDOWN:
                if self.selected and not (self.grid[self.selected[1]][self.selected[0]].locked):
                    if self.is_legal_input(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]].value = int(event.unicode)
                        self.selected = None

    def update(self) -> None:
        """
        DESCRIPTION
        updates for background functionality each game step
        """
        self.mouse_position = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(self.mouse_position)

    def draw(self) -> None:
        """
        DESCRIPTION
        draws everything to the window surface each step of the game
        """
        self.window.fill(WHITE)
        self.draw_buttons()
        if (self.selected): self.draw_selection()
        self.draw_grid()
        self.draw_grid_numbers()
        self.draw_titles()
        pygame.display.update()

    def draw_buttons(self) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the GUI buttons
        """
        for button in self.buttons:
            button.draw(self.window)

    def draw_selection(self) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the selected cell highlight
        """
        pygame.draw.rect(self.window, HIGHLIGHT, 
            (self.grid_x + (self.selected[0] * CELL_WIDTH) + self.selected[0],
             self.grid_y + (self.selected[1] * CELL_HEIGHT) + self.selected[1],
             CELL_WIDTH, CELL_HEIGHT))

    def draw_grid(self) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the game puzzle grid
        """
        cell_x_offset = 0
        cell_y_offset = 0
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                current_cell = self.grid[i][j]
                if current_cell.locked:
                    # "Brick" Cell
                    pygame.draw.rect(self.window, DARK, (self.grid_x + cell_x_offset, self.grid_y + cell_y_offset, CELL_WIDTH, CELL_HEIGHT))
                    pygame.draw.line(self.window, MEDIUM, (self.grid_x + cell_x_offset, self.grid_y + cell_y_offset), (self.grid_x + cell_x_offset + CELL_WIDTH, self.grid_y + cell_y_offset + CELL_HEIGHT))
                else:
                    # "Empty" Cell
                    pygame.draw.rect(self.window, DARK, (self.grid_x + cell_x_offset, self.grid_y + cell_y_offset, CELL_WIDTH, CELL_HEIGHT), 1)
                cell_x_offset += CELL_WIDTH + 1
            cell_x_offset = 0
            cell_y_offset += CELL_HEIGHT + 1

    def draw_grid_numbers(self) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the game puzzle grid numbers
        """
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                current_cell = self.grid[i][j]
                if not current_cell.locked and current_cell.value:
                    position = (self.grid_x + (j * CELL_WIDTH) + j, self.grid_y + (i * CELL_HEIGHT) + i)
                    self.draw_text(str(current_cell.value), position, DARK)
                else:
                    position = (self.grid_x + (j * CELL_WIDTH) + j, self.grid_y + (i * CELL_HEIGHT) + i)
                    self.draw_headers(str(current_cell.down if current_cell.down else ""), str(current_cell.across if current_cell.across else ""), position, WHITE)

    def draw_titles(self) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the titles, subtitles, and headers
        """
        # Title
        image = TITLE_FONT.render("Cross Sum", True, ACCENT_2)
        image_x_offset = (WINDOW_WIDTH // 2) - (image.get_width() // 2)
        self.window.blit(image, (image_x_offset, 25))
        # Subtitle
        image = SUBTITLE_FONT.render("by Alex Muñoz", True, ACCENT_1)
        image_x_offset = (WINDOW_WIDTH // 2) - (image.get_width() // 2)
        self.window.blit(image, (image_x_offset, 60))
        # Difficulty
        image = HEADER_FONT.render(self.difficulty, True, ACCENT_1)
        self.window.blit(image, (92, 455))
        # Banner
        image = SUBTITLE_FONT.render(self.banner, True, self.banner_color)
        image_x_offset = (WINDOW_WIDTH // 2) - (image.get_width() // 2)
        self.window.blit(image, (image_x_offset, 100))

    def draw_text(self, text : str, position : tuple, color : tuple) -> None:
        """
        DESCRIPTION
        a helper function used to draw text to a surface at a given position
        """
        image = NUMBER_FONT.render(text, True, color)
        image_width = image.get_width()
        image_height = image.get_height()
        # Adjust position to center text
        position_x = position[0] + (CELL_WIDTH - image_width) // 2
        position_y = position[1] + (CELL_HEIGHT - image_height) // 2
        position = (position_x, position_y)
        self.window.blit(image, position)

    def draw_headers(self, down_value : int, across_value: int, position: tuple, color : tuple) -> None:
        """
        DESCRIPTION
        a helper function for the draw function which draws the puzzle grid headers
        """
        # Set Up Down Header
        image = HEADER_FONT.render(down_value, True, color)
        image_width = image.get_width()
        image_height = image.get_height()
        # Draw Down Header
        position_x = position[0] + (CELL_WIDTH - image_width) // 4
        position_y = position[1] + (CELL_HEIGHT - image_height) * .75
        self.window.blit(image, (position_x, position_y))
        
        # Set Up Across Header
        image = HEADER_FONT.render(across_value, True, color)
        image_width = image.get_width()
        image_height = image.get_height()
        # Draw Across Header
        position_x = position[0] + (CELL_WIDTH - image_width) * .75
        position_y = position[1] + (CELL_HEIGHT - image_height) // 4
        self.window.blit(image, (position_x, position_y))

    def get_mouseover_grid_cell(self) -> tuple:
        """
        DESCRIPTION
        returns the position of the mouse in the puzzle grid
        """
        # Check if mouse is in grid
        if (self.mouse_position[0] < self.grid_x) or (self.mouse_position[1] < self.grid_y):
            return None
        if (self.grid_x + self.grid_pixel_width < self.mouse_position[0]) or (self.grid_y + self.grid_pixel_height < self.mouse_position[1]):
            return None
        # Mouse in grid
        return int((self.mouse_position[0] - self.grid_x) // CELL_WIDTH), int((self.mouse_position[1] - self.grid_y) // CELL_HEIGHT)

    def is_legal_input(self, input_value) -> bool:
        """
        DESCRIPTION
        Checks whether the user is inputting a valid value.
        """
        try:
            if 0 < int(input_value) < 10:
                return True
            else:
                return False
        except:
            return False
#endregion