import pygame
import time
import copy
from SudokuPuzzleSolver import PuzzleInterface
from ButtonTxtRsc import TextResources
from ConfigFiles import configvideo, configcolor

# -------------+
pygame.init()  #
# -------------+


class Board:

    def __init__(self):
        self.row_len = 9
        self.col_len = 9
        self.margin = 5
        self.bandaid = 1  # This is to fix buttons under or overdrawn by 1 pixel. Make it 0 to see why.
        self.puzzle_index = -1

        self.board = None
        self.board_solved = None
        self.board_is_solved = False
        self.puzzle_as_file = None
        self.difficulty = None

        self.submenu = None
        self.button_next = None
        self.button_previous = None
        self.elapsed_start = None

    def initialize_board(self):

        offset = 8  # For micro-pixel adjustment- if full-screen is NOT desired
        w = (window.get_width() // self.row_len) - (self.margin+offset)
        h = (window.get_height() // self.col_len) - (self.margin+offset)

        self._choose_puzzle()
        self._set_tile_properties(0, 0, w, h)

        h += offset
        self._set_submenu_properties(0, window.get_height()-h, window.get_width(), h)

        h -= offset
        self._set_sidemenu_properties(window.get_width()-w-(self.margin+self.bandaid), 0, w, (h * 3) + (self.margin*2+self.bandaid))
        self.elapsed_start = time.perf_counter()

    def validate_solution(self):

        # Return if board contains any 0s / is incomplete
        for row in self.board:
            for button in row:
                if button.text == " " or button.text == "":
                    return

        user_board_copy = copy.copy(self.board)
        self.board = puzzle_interface.format_board_manually(self.board)

        if self.board == self.board_solved:
            self._process_next_board(user_board_copy)
        else:
            self.board = user_board_copy

    def _process_next_board(self, board_to_update):

        self.board_is_solved = True
        for row in board_to_update:
            for button in row:
                button.update_color(colors.tile_solved)

    def update_tile(self, button):

        if self.board_is_solved:
            return

        valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = self._index_selector(valid_numbers, button)
        number = valid_numbers[index]
        button.update_text(number)
        button.update_color(colors.tile_selected)

    def _index_selector(self, data_set, button):

        if button.text == "" or button.text == " ":
            return 0
        else:
            i = data_set.index(int(button.text)) + 1
            if i >= len(data_set):
                return 0
            else:
                return i

    def _choose_puzzle(self):
        self.puzzle_index += 1
        self.puzzle_file = puzzle_interface.get_a_csci4463_puzzle_file(self.puzzle_index)
        self.difficulty = puzzle_interface.get_csci4463_puzzle_difficulty(self.puzzle_file)
        self.board = puzzle_interface.read_puzzle_from_file(self.puzzle_file)
        self.board_solved = puzzle_interface.solve_puzzle_with_backtracking(puzzle_interface.read_puzzle_from_file(self.puzzle_file))

    def _set_tile_properties(self, x, y, w, h):

        """
        :param x: X position of first tile (0 is recommended)
        :param y: Y position of first tile (also recommend 0)
        Note: X and Y positions are automatically adjusted
        :param w: Width size of individual tile
        :param h: Height size of individual tile
        :return: properties of each tile
        """

        dividers = []  # It helps to draw the dividers after tiles are drawn
        for r, row in enumerate(self.board):
            for t, tile in enumerate(row):

                # Show no button text if value is 0
                if int(tile) == 0:
                    tile = " "

                # Create & draw a button on each loop
                button = Button(str(tile), colors.tile_default, x, y, w, h)  # 2)
                button.draw(window)

                # Replace individual board tile with tuple of critical information
                self.board[r][t] = button

                # Offset the next tile position using the following guessed formula:
                x = x + (self.margin+w)

                # Create 2 horizontal and vertical line dividers:
                # 1 - We only need one iteration of lines (it's in this loop for easy access to info)
                # 2 - It's a multiple of 3 (except for 0)
                if (r == 0) and (t % 3 == 0 and t != 0):
                    position = x - w - (self.margin*2)  # Note: I don't know why this works for both x and y
                    column_vertical = Button("", colors.grey_light, position, 0, self.margin, window.get_height())
                    column_horizontal = Button("", colors.grey_light, 0, position, window.get_width(), self.margin)
                    dividers.append(column_vertical)
                    dividers.append(column_horizontal)

            # Reset x and y positions when we reach a new row
            y = y + (self.margin+h)
            x = 0

        # Finally, draw the dividers as a cosmetic
        for divider in dividers:
            divider.draw(window)

    def _set_submenu_properties(self, x, y, w, h):
        self.submenu = Button(f"", colors.submenu, x, y, w+self.margin+2, h)
        self.submenu.draw(window, None, 40, True)

    def _set_sidemenu_properties(self, x, y, w, h):

        """
        :param x: recommended: window.get_width() + or - other calculations
        :param y: recommended: 0
        :param w: width of side menu
        :param h: height of side menu
        :return: individual button pieces being drawn
        """

        # TODO: These micro-pixel adjustments are probably
        # going to break if the window is resized

        w += self.bandaid+self.bandaid
        h += self.bandaid+self.bandaid

        button1 = Button(f"Puzzle:", colors.side_menu, x, y, w, h // 2)
        button1.draw(window, None, 30, False)
        button2 = Button(f"{self.puzzle_file}", colors.side_menu, x, (h // 2), w, h // 2)
        button2.draw(window, None, 25, False)
        button3 = Button(f"Best time:", colors.side_menu, x, h, w, (h+self.margin) // 2)
        button3.draw(window, colors.black, 24, False)
        button4 = Button(f"WIP", colors.side_menu, x, h + button3.h, w, (h + self.margin) // 2)
        button4.draw(window, None, 24, False)
        button5 = Button(f"Cycle", colors.submenu, x, h * 2 + 2, w, (h + self.margin) // 3)
        button5.draw(window, colors.black, 24, False)

        self.button_next = Button(f"-->", colors.submenu, x+self.margin, (h * 2 + 2) + w + (self.margin*3) + self.margin, w - (self.margin*2), ((h + self.margin) // 3) - (self.margin*6))
        self.button_next.draw(window, colors.grey_discord, 24, False)

        self.button_previous = Button(f"<--", colors.submenu, x+self.margin, (h * 2 + 2) + w * 2 + self.margin, w - (self.margin*2), ((h + self.margin) // 3) - (self.margin*6))
        self.button_previous.draw(window, colors.grey_discord, 24, False)

    def update_submenu_text(self):
        if self.board_is_solved:
            return
        board.submenu.update_text(f"Puzzle {self.puzzle_index+1}/{len(puzzle_interface.get_all_csci4463_puzzle_files())} | Difficulty: {board.difficulty} | Time elapsed: {round(time.perf_counter()-self.elapsed_start)}", 40)

    def update_submenu_buttons(self, mouse_pos):
        if self.button_next.is_over(mouse_pos):
            self.button_next.update_color(colors.tile_hovering)
        else:
            self.button_next.update_color(colors.submenu)

        if self.button_previous.is_over(mouse_pos):
            self.button_previous.update_color(colors.tile_hovering)
        else:
            self.button_previous.update_color(colors.submenu)

    def get_button_from_mouse_pos(self, mouse_pos):

        for row in self.board:
            for button in row:
                if button.is_over(mouse_pos):
                    return button

    def __dir__(self):

        """
        :return: each individual button for debugging purposes
        """

        for row in self.board:
            for button in row:
                print(button.text)


class Menu:

    def __init__(self):
        self.is_main_menu = True
        self.is_settings_menu = False
        self.is_game_screen = False

    def draw_main_menu(self, mouse_pos):

        # MouseMotion events
        if event.type == pygame.MOUSEMOTION:
            if button_main.is_over(mouse_pos):
                if button_main.text == txt_rsrcs.play:
                    button_main.update_color(colors.green)
            else:
                button_main.update_color(colors.red)
                button_main.update_text(txt_rsrcs.play)

            if button_settings.is_over(mouse_pos):
                if button_settings.text == txt_rsrcs.settings:
                    button_settings.update_color(colors.green)
            else:
                button_settings.update_color(colors.red)
                button_settings.update_text(txt_rsrcs.settings)

        # MouseButtonDown events - load game screens here
        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_main.is_over(mouse_pos):
                self._load_game_menu()

            if button_settings.is_over(mouse_pos):
                self._load_settings_menu()

    def draw_settings_menu(self, mouse_pos):
        pass

    def draw_game_screen(self, mouse_pos):

        if board.board_is_solved:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = board.get_button_from_mouse_pos(mouse_pos)
            if button:
                if button.text == " " or button.text == "":
                    board.update_tile(button)
                elif button.color == colors.tile_selected:
                    board.update_tile(button)
            board.validate_solution()

    def _load_main_menu(self):
        pass

    def _load_settings_menu(self):
        self.is_main_menu = False
        self.is_settings_menu = True
        self.is_game_screen = False
        button_settings.update_color(colors.blue)
        button_settings.update_text(txt_rsrcs.clicked)

    def _load_game_menu(self):
        self.is_main_menu = False
        self.is_settings_menu = False
        self.is_game_screen = True
        window.fill(colors.black)
        pygame.display.flip()

        # -----------------------+
        board.initialize_board()  #
        # -----------------------+


class Button:

    def __init__(self, text, color, x_pos, y_pos, width, height):
        self.text = text
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.w = width
        self.h = height

    def draw(self, surface, outline=None, text_size=None, xcenter=False):
        """
        Draws the button on the screen
        :param surface: the window/surface to draw on
        :param outline: outline color, if any
        :param text_size: size of button text
        :param xcenter: center this button on the x-axis? False by default
        """
        if xcenter:
            self.x = (surface.get_width() // 2) - (self.w // 2) - 4

        if outline:
            # x = self.x-4
            x = self.x-4
            y = self.y-4
            w = self.w+8
            h = self.h+8
            pygame.draw.rect(surface, outline, (x, y, w, h), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text != '':

            if text_size is None:
                text_size = 60
            else:
                text_size = text_size

            font = pygame.font.SysFont('comicsans', text_size)
            text = font.render(self.text, 1, colors.white)
            center = (self.x + (self.w//2 - text.get_width()//2), self.y + (self.h//2 - text.get_height()//2))
            surface.blit(text, center)

        # -----------------------+
        pygame.display.update()  #
        # -----------------------+

    def is_over(self, position):
        if self.x < position[0] < self.x + self.w:
            if self.y < position[1] < self.y + self.h:
                return True
        return False

    def update_color(self, color, outline=None):

        """
        :param color: update the color of the button
        :param outline: this is assuming the button doesn't already have an outline
        :return: the button drawn on the window surface
        """

        self.color = color
        self.draw(window, outline)

    def update_text(self, text, text_size=None):

        if type(text) != str:  # Useful if integers are passed through
            text = str(text)

        self.text = text
        self.draw(window, None, text_size, False)


def text_objects(text, config):
    surface = config.render(text, True, colors.white)
    rectangle = surface.get_rect()
    return surface, rectangle


def display_text(text):
    font_size_config = pygame.font.Font(graphics.font_type, graphics.font_size)
    text_surface, text_rectangle = text_objects(text, font_size_config)
    text_rectangle.center = ((800//2), 100)
    window.blit(text_surface, text_rectangle)
    pygame.display.update()


graphics = configvideo
colors = configcolor
menu = Menu()
board = Board()
txt_rsrcs = TextResources()
puzzle_interface = PuzzleInterface()

window = pygame.display.set_mode(graphics.resolution)
window.fill(colors.grey_discord)
pygame.display.set_caption(graphics.caption)
display_text("Ultimate Suduoku Puzzles")

button_main = Button(txt_rsrcs.play, colors.red, window.get_width() // 2, window.get_height() // 2, 250, 100)
button_main.draw(window, colors.black, None, True)
button_settings = Button(txt_rsrcs.settings, colors.grey_discord, window.get_width() // 2, (window.get_height() // 2) + 150, 250, 100)
button_settings.draw(window, colors.black, None, True)

# ---------------------+
pygame.display.flip()  #
# ---------------------+


running = True
while running:

    # ---------------------------------------+
    mouse_position = pygame.mouse.get_pos()  #
    # ---------------------------------------+

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()  # TODO: Some people recommend this. Necessary?
            quit()  # And why this?

        if menu.is_main_menu:
            menu.draw_main_menu(mouse_position)
        elif menu.is_game_screen:
            menu.draw_game_screen(mouse_position)
        elif menu.is_settings_menu:
            menu.draw_settings_menu(mouse_position)
        else:
            running = False
            pygame.quit()
            quit()

    if menu.is_game_screen:
        board.update_submenu_text()
        board.update_submenu_buttons(mouse_position)

