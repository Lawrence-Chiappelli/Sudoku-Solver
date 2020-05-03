"""
MIT License

Copyright (c) 2020 Lawrence Chiappelli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame
import time
import copy
import sys
from SudokuPuzzleSolver import PuzzleInterface
from Resources.Strings import ButtonTxt
from Resources.ConfigFiles import configcolor, configvideo, configkeypadcode

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
        self.board_solution = None
        self.board_is_solved = False
        self.board_is_dual_solving = False

        # Submenu items
        self.button_submenu = None  # Individual button
        self.puzzle_as_file = None
        self.difficulty = None
        self.elapsed_start = None
        self.num_total_puzzles = 45  # TODO: Where to soft code?

        # Side menu
        self.button_auto_solve = None  # Solve button
        self.button_next = None  # Next button
        self.button_previous = None  # Previous button

        # Tile selection mode
        self.click_to_type = True
        self.active_tile = None

    def initialize_board(self, forward=True):

        """
        :param forward: indicate file selection direction (next or previous)
        :return: None

        self.board_is_solved and self.board_solution should also be reset here.
        These values are re-used when the player selects the next puzzle.
        """

        offset = 8  # For micro-pixel adjustment- if full-screen is NOT desired
        w = (window.get_width() // self.row_len) - (self.margin+offset)
        h = (window.get_height() // self.col_len) - (self.margin+offset)

        direction_index = self._get_puzzle_direction(forward)
        self.board = self._choose_puzzle(direction_index)
        self.board_is_solved = False
        self.board_solution = None

        # -------------------------------------+
        self._set_tile_properties(0, 0, w, h)  #
        # -------------------------------------+

        h += offset
        self._set_submenu_properties(0, window.get_height()-h, window.get_width(), h)

        h -= offset
        self._set_sidemenu_properties(window.get_width()-w-(self.margin+self.bandaid), 0, w, (h * 3) + (self.margin*2+self.bandaid))

        self.elapsed_start = time.perf_counter()

    def validate_solution(self):

        # Return if board contains any 0s / is incomplete
        if not self.board_is_dual_solving:
            for row in self.board:
                for button in row:
                    if button.text == " " or button.text == "":
                        return

        # Start solving the board in a separate solution
        if self.board_solution is None:
            self.button_submenu.update_text(txt_rsrcs.solving)
            self.button_submenu.update_color(colors.grey)

            puzzle_og = puzzle_interface.read_puzzle_from_file(self.puzzle_file)  # Original file to read from
            if self.board_is_dual_solving:
                self.board_solution = puzzle_interface.solve_puzzle_with_backtracking(puzzle_og, self.board)
            else:
                self.board_solution = puzzle_interface.solve_puzzle_with_backtracking(puzzle_og)
            self.button_submenu.update_color(colors.submenu)

        if self.board_is_dual_solving:
            self.board_is_solved = True
            self._process_solved_board()
        elif self.board_solution == copy.copy(puzzle_interface.format_board_manually(self.board)):
            self.board_is_solved = True
            self._process_solved_board()
        else:
            print(f"Incorrect solution:\n{self.board}\nvs\n{self.board_solution}")

    def update_tile(self, button, user_input):

        """
        :param button: the tile button
        :param user_input: which mouse button the user pressed
        :return: None

        First determines which method of tile selection.
        TODO: Functionality to activate _cycle_tile
        """

        if self.board_is_solved:
            return None

        if self.click_to_type:
            self._type_tile(button, user_input)
        else:
            self._cycle_tile(button, user_input)

    def clear_tile(self, tile_to_clear):

        """
        :param tile_to_clear: the tile to restore to its original properties
        :return: none
        """

        tile_to_clear.update_text("")
        tile_to_clear.update_color(colors.tile_default)
        self.active_tile = None

    def _type_tile(self, button, user_input):

        """
        :param button: button to set or clear as active tile
        :param user_input: should be a keyboard press
        :return: None
        """

        if self.active_tile is None:
            self.active_tile = button
            button.update_color(colors.tile_selected)
        else:
            value = translator.translate_pygame_keypadcode(user_input)
            if value:
                self.active_tile.update_text(value)
                self.active_tile.update_color(colors.tile_confirmed)
                self.active_tile = None
            elif user_input == 127:  # 127 is delete key
                self.clear_tile(button)

    def _cycle_tile(self, button, user_input):
        valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = self._tile_number_index_selector(valid_numbers, button, user_input)
        number = valid_numbers[index]
        button.update_text(number)
        button.update_color(colors.tile_selected)

    def _tile_number_index_selector(self, data_set, button, direction):

        """
        :param data_set: to grab the raw data from the set and with direction
        :param button: the tile's properties to update
        :param direction: pygame left-click is 1, middle click is 2, right click is 3
        :return: the index, and use it to display the appropriate tile number
        """

        pygame_leftclick = 1
        if direction != pygame_leftclick:
            direction = -1

        if button.text == "" or button.text == " ":
            return 0
        else:
            i = data_set.index(int(button.text)) + direction
            if i >= len(data_set):
                return 0
            else:
                return i

    def _get_puzzle_direction(self, forward):

        """
        :param forward: return incrementer if forward, decremented if backward
        :return: index incrementer for next puzzle selection
        Note: only find the total number of puzzles once
        This seems to be the most optimal place
        """

        if forward:
            if self.puzzle_index < self.num_total_puzzles:
                return 1
        else:
            if self.puzzle_index != 0:
                return -1
        return 0

    def _choose_puzzle(self, direction):

        self.puzzle_index += direction
        self.puzzle_file = puzzle_interface.get_a_csci4463_puzzle_file(self.puzzle_index)
        self.difficulty = puzzle_interface.get_csci4463_puzzle_difficulty(self.puzzle_file)
        return puzzle_interface.read_puzzle_from_file(self.puzzle_file)

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
                    tile = ""

                # Create & draw a button on each loop
                button = Button(str(tile), graphics.get_font_size(), colors.tile_default, x, y, w, h)  # 2)
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
                    column_vertical = Button("", None, colors.grey_light, position, 0, self.margin, window.get_height())
                    column_horizontal = Button("", None, colors.grey_light, 0, position, window.get_width(), self.margin)
                    dividers.append(column_vertical)
                    dividers.append(column_horizontal)

            # Reset x and y positions when we reach a new row
            y = y + (self.margin+h)
            x = 0

        # Finally, draw the dividers as a cosmetic
        for divider in dividers:
            divider.draw(window)

    def _set_submenu_properties(self, x, y, w, h):
        self.button_submenu = Button(f"", graphics.get_font_size(30), colors.submenu, x, y, w + self.margin + 2, h)
        self.button_submenu.draw(window, None, True)
        return None

    def _set_sidemenu_properties(self, x, y, w, h):

        """
        :param x: recommended: window.get_width() + or - other calculations
        :param y: recommended: 0
        :param w: width of side menu
        :param h: height of side menu
        :return: nothing, every side menu property is drawn here
        """

        # TODO: These micro-pixel adjustments are probably
        # going to break if the window is resized.
        # Is this the naive solution?

        bandaid = self.bandaid + self.bandaid  # 2 seemed to the sweet spot for these buttons
        w += bandaid
        h += bandaid

        button1 = Button(txt_rsrcs.puzzle, graphics.get_font_size(20), colors.side_menu, x, (y+self.margin) // bandaid, w, (h // bandaid) - self.margin)
        button1.draw(window, colors.black, False)
        button2 = Button(self.puzzle_file, graphics.get_font_size(18), colors.side_menu, x, (h // bandaid), w, (h // bandaid) - bandaid)
        button2.draw(window, colors.black, False)
        button3 = Button(txt_rsrcs.cycle, graphics.get_font_size(20), colors.submenu, x, h * bandaid + bandaid, w, (h + self.margin) // 3)  # Make this 3 a 2 to revert to half size
        button3.draw(window, colors.black, False)

        self.button_auto_solve = Button(txt_rsrcs.auto_solve, graphics.get_font_size(15), colors.submenu, x + self.margin, h + (self.margin * 11), w - (self.margin * bandaid), (h - self.margin) // bandaid)
        self.button_auto_solve.draw(window, colors.grey, False)
        self.button_next = Button(txt_rsrcs.arrow_next, graphics.get_font_size(), colors.submenu, x+self.margin, (h * bandaid + bandaid) + w + (self.margin*3) + self.margin, w - (self.margin*bandaid), ((h + self.margin) // 3) - (self.margin*6))
        self.button_next.draw(window, colors.grey_discord, False)
        self.button_previous = Button(txt_rsrcs.arrow_previous, graphics.get_font_size(), colors.submenu, x+self.margin, (h * bandaid + bandaid) + w * bandaid + self.margin, w - (self.margin*bandaid), ((h + self.margin) // 3) - (self.margin*6))
        self.button_previous.draw(window, colors.grey_discord, False)
        return None

    def _process_solved_board(self):

        """
        :return: None

        Handles colors and otherwise cosmetics
        to indicate successful board completion

        Note: The player must click the
        cycle arrow to start a new puzzle.
        """

        if self.board_is_dual_solving:
            self.board_is_dual_solving = False

        for row in self.board:
            for button in row:
                button.update_color(colors.tile_solved, colors.black)
        self.button_submenu.update_color(colors.puzzle_solved)

        time_completed = round(time.perf_counter()-self.elapsed_start)
        self.button_submenu.update_text(f"PUZZLE SOLVED! | Time to complete: {time_completed} seconds")

    def update_submenu(self):

        """
        Submenu: Puzzle | Difficulty | Time
        :return: None

        This method handles updating the submenu
        timer. Ideally, this should be called
        every frame, *regardless of events*
        to ensure that the time is
        being reflected accurately.
        """

        if self.board_is_solved:  # Stop updating this particular text is the user solved the board
            return

        text = f"Puzzle {self.puzzle_index+1}/{len(puzzle_interface.get_all_csci4463_puzzle_files())} | Difficulty: {board.difficulty} | Time elapsed: {round(time.perf_counter()-self.elapsed_start)}"
        board.button_submenu.update_text(text)

    def update_side_menu(self, mouse_pos):

        """
        Side menu: Puzzle file | Auto Solve | Next/previous
        :param mouse_pos: (x, y) position of mouse
        :return: None

        Note: the reason for having this method
        outside of def draw_game_screen() is due
        to the *timing* of button colors being drawn.

        Should this be inside draw_game_screen(), the
        hover highlight effect will disappear after
        the player clicks the button. Ideally, the
        highlight color should remain after the button
        is clicked, not be reset to default.

        This method update every frame, as opposed
        to when pygame detects an event. In essence:
        the highlight color will remain after
        the button is clicked.
        """

        # Button - auto solve
        if not self.board_is_dual_solving:
            if self.button_auto_solve.is_over(mouse_pos):
                self.button_auto_solve.update_color(colors.green)
            else:
                self.button_auto_solve.update_color(colors.submenu)

            # Button - next puzzle
            if self.button_next.is_over(mouse_pos):
                self.button_next.update_color(colors.tile_hovering)
            else:
                self.button_next.update_color(colors.submenu)

            # Button - previous puzzle
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

        # MouseMotion - Adjust colors when hovering
        if event.type == pygame.MOUSEMOTION:

            # Button - play
            if button_main.is_over(mouse_pos):
                if button_main.text == txt_rsrcs.play:
                    button_main.update_color(colors.green)
            else:
                button_main.update_color(colors.tile_default)
                button_main.update_text(txt_rsrcs.play)

            # Button - settings
            if button_settings.is_over(mouse_pos):
                if button_settings.text == txt_rsrcs.settings:
                    button_settings.update_color(colors.green)
            else:
                button_settings.update_color(colors.tile_default)
                button_settings.update_text(txt_rsrcs.settings)

        # MouseButtonDown - loads game screens
        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_main.is_over(mouse_pos):
                self._load_game_menu()

            if button_settings.is_over(mouse_pos):
                self._load_settings_menu()

    def draw_settings_menu(self, mouse_pos):
        pass

    def draw_game_screen(self, mouse_pos):

        if board.board_is_dual_solving:
            return

        # See def update_side_menu() for side menu buttons.
        # The reasoning for this is critical to understand.

        #  MouseButtonDown - Execute tile / sub/side menu functionality
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Button - auto solve
            if board.button_auto_solve.is_over(mouse_pos) and board.active_tile is None:
                board.board_is_dual_solving = True
                board.validate_solution()

            # Button - next puzzle
            elif board.button_next.is_over(mouse_pos):
                board.initialize_board()

            # Button - previous puzzle
            elif board.button_previous.is_over(mouse_pos):
                board.initialize_board(False)
            else:
                button = board.get_button_from_mouse_pos(mouse_pos)
                if button:
                    if event.button == 1:  # Left click
                        if button.text == " " or button.text == "" or button.color == colors.tile_confirmed:
                            board.update_tile(button, event.button)
                    elif event.button == 3:  # Right click
                        if button.color == colors.tile_selected or button.color == colors.tile_confirmed:
                            board.clear_tile(button)

        # KeyDown - To type in a number for an active tile
        if event.type == pygame.KEYDOWN:
            if board.active_tile is None:
                return
            else:
                board.update_tile(board.active_tile, event.key)
                board.validate_solution()

    def _load_main_menu(self):
        pass

    def _load_settings_menu(self):
        # self.is_main_menu = False
        # self.is_settings_menu = True
        self.is_game_screen = False
        button_settings.update_color(colors.blue)
        button_settings.update_text(txt_rsrcs.wip)

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

    def __init__(self, text, text_size, color, x_pos, y_pos, width, height):
        self.text = text
        self.text_size = text_size
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.w = width
        self.h = height

    def draw(self, surface, outline=None, xcenter=False):
        """
        Draws the button on the screen
        :param surface: the window/surface to draw on
        :param outline: outline color, if any
        :param xcenter: center this button on the x-axis? False by default
        TODO: optional parameter for font type override?
        """
        if xcenter:
            self.x = (surface.get_width() // 2) - (self.w // 2) - 4

        """
        Draw rectangles:
        """
        if outline:
            x = self.x-4
            y = self.y-4
            w = self.w+8
            h = self.h+8
            pygame.draw.rect(surface, outline, (x, y, w, h), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h), 0)

        """
        Draw text:
        """
        if self.text != "" or self.text_size is not None:

            font = pygame.font.Font("Resources/Fonts/FreeSansBold-Xgdd.ttf", self.text_size)
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

        Hint: changing color alone won't update it-
        you need to constantly draw it.
        """

        self.color = color
        self.draw(window, outline)

    def update_text(self, text):

        """
        :param text: string text of button
        :return: None

        TODO: Functionality to dynamically update text size
        """

        if type(text) != str:  # Useful if integers are passed through
            text = str(text)

        self.text = text
        self.draw(window, None, False)


def text_objects(text, config):
    surface = config.render(text, True, colors.white)
    rectangle = surface.get_rect()
    return surface, rectangle


def display_text(text):

    font_size_config = pygame.font.Font("Resources/Fonts/FreeSansBold-Xgdd.ttf", graphics.get_font_size())
    text_surface, text_rectangle = text_objects(text, font_size_config)
    text_rectangle.center = ((800//2), 100)
    window.blit(text_surface, text_rectangle)
    pygame.display.update()


graphics = configvideo.VideoConfig()
colors = configcolor
translator = configkeypadcode
menu = Menu()
board = Board()
txt_rsrcs = ButtonTxt
puzzle_interface = PuzzleInterface()

window = pygame.display.set_mode(graphics.get_resolution())
window.fill(colors.grey_discord)
pygame.display.set_caption(txt_rsrcs.caption)
display_text(txt_rsrcs.main_menu_title)

button_main = Button(txt_rsrcs.play, graphics.get_font_size(), colors.tile_default, window.get_width() // 2, window.get_height() // 2, 250, 100)
button_main.draw(window, colors.black, True)
button_settings = Button(txt_rsrcs.settings, graphics.get_font_size(), colors.tile_default, window.get_width() // 2, (window.get_height() // 2) + 150, 250, 100)
button_settings.draw(window, colors.black, True)

# ---------------------+
pygame.display.flip()  #
# ---------------------+

running = True
while running:

    # Don't accept any frame drawing if computer is busy
    if not board.board_is_dual_solving:

        # ---------------------------------------+
        mouse_position = pygame.mouse.get_pos()  #
        # ---------------------------------------+

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if menu.is_main_menu:
                menu.draw_main_menu(mouse_position)
            elif menu.is_game_screen:
                menu.draw_game_screen(mouse_position)
            elif menu.is_settings_menu:
                menu.draw_settings_menu(mouse_position)

        if menu.is_game_screen:

            """
            It's critical that these events
            update every frame (as opposed to
            when pygame detects an event- which
            means not every frame)
            """

            # ------------------------------------- #
            board.update_submenu()                  #
            board.update_side_menu(mouse_position)  #
            # ------------------------------------- #
