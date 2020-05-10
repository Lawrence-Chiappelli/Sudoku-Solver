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

import os
import warnings
import copy
import re
import pygame
import sys
from Resources.ConfigFiles import configcolor as colors


class PuzzleInterface:

    def __init__(self):
        self.all_puzzle_files = [puzzlefile for puzzlefile in os.listdir("CSCI4463SudokuPuzzles") if puzzlefile.endswith(".txt")]
        self.gui = None

    def get_all_csci4463_puzzle_files(self):
        return self.all_puzzle_files

    def get_a_csci4463_puzzle_file(self, index):
        return self.all_puzzle_files[index]

    def get_csci4463_puzzle_difficulty(self, puzzlefile):

        easy_puzzles = ["01", "02", "06", "10", "13"]
        medium_puzzles = ["03", "04", "07", "11", "14"]
        hard_puzzles = ["05", "08", "09", "12", "15", "16"]

        file_difficulty = re.search(r"\d+", puzzlefile).group(0)
        if file_difficulty in easy_puzzles:
            return "Easy"
        elif file_difficulty in medium_puzzles:
            return "Medium"
        elif file_difficulty in hard_puzzles:
            return "Hard"
        else:
            warnings.warn("Unable to detect each file's difficulty based on the current working environment.", Warning)
            return "N/A - Could not determine difficulty"

    def solve_puzzle_with_backtracking(self, source_puzzle, gui=None):

        """
        :param source_puzzle: converted puzzle- as a *LIST*
        :param gui: original board without conversion, if using a GUI
        :return: the solved puzzle- as a *STRING*
        """

        # Prevent window GUI crashes
        # ---------------------------+
        self._balance_event_queue()  #
        # ---------------------------+

        empty_tile = self._get_tile_position(source_puzzle)
        if self.gui is None and gui:
            self.gui = gui

        if empty_tile is None:
            return source_puzzle
        else:
            row_pos, col_pos = empty_tile

        for test_val in range(1, 10):
            if self._check_newval_validity(row_pos, col_pos, test_val, source_puzzle):
                source_puzzle[row_pos][col_pos] = test_val
                self._update_gui_tile(row_pos, col_pos, colors.tile_default, colors.green, test_val)

                if self.solve_puzzle_with_backtracking(source_puzzle, None):
                    return self._to_string_board_source(source_puzzle)

                # This is backtracking- here, *RESET* the tile to 0 if the given solutions do not work.
                # ---------------------------------- +
                source_puzzle[row_pos][col_pos] = 0  #
                # -----------------------------------+
                self._update_gui_tile(row_pos, col_pos, colors.tile_default, colors.red, test_val)

        return False

    def read_puzzle_from_file(self, file):
        try:
            with open(f"CSCI4463SudokuPuzzles/{file}", "r") as file_contents:
                puzzle = file_contents.read()
                return self.from_string_to_list(puzzle)
        except FileNotFoundError as fnfe:
            warnings.warn(f"Files were not found:\n{fnfe}\n\nLast check for files- searching root directory...", UserWarning)
            with open(file, "r") as puzzle:
                return self.from_string_to_list(puzzle)

    def to_string_gui_board(self, puzzle):

        """
        :param puzzle: must contain PyGame button objects
        :return: the formatted board used to compare STRING solution

        fdsa
        """

        user_board = []
        for row in puzzle:
            local_row = []
            for button in row:
                try:
                    if button.text == " " or button.text == "":
                        local_row.append(0)
                    else:
                        local_row.append(int(button.text))
                except TypeError as te:
                    raise TypeError(f"Wrong format for final conversion! The board being passed through must contain button objects. Traceback:\n{te}")
            user_board.append(copy.copy(local_row))
        user_board = self._to_string_board_source(user_board)
        return user_board

    def from_string_to_list(self, puzzle):

        """
        :param puzzle: useful for converting converted puzzle solutions
        back into a list for iteration purposes.
        :return: the board as a 2d array / 2d list
        """

        if type(puzzle) != str:
            raise TypeError("_from_string_to_list takes a string puzzle!\nDouble check your conversions.")

        new_board = []
        row = []
        position = 0
        for tile in puzzle:
            if position == 9:
                new_board.append(copy.copy(row))
                row.clear()
                position = 0
            if str(tile).isdigit():
                row.append(int(tile))
                position += 1

        return new_board

    def _to_string_board_source(self, puzzle):

        """
        :param puzzle:
        :return: board rows *indented*

        This takes a source board, not a GUI board.
        """

        organized = ""
        for row in puzzle:
            organized += f"\n{row}"
        return organized

    def _update_gui_tile(self, row, col, color, color_outline, text):

        if self.gui is None:
            return

        clock = pygame.time.Clock()
        clock.tick(15)
        self.gui[row][col].update_color(color, color_outline)
        self.gui[row][col].update_text(text)

    def _balance_event_queue(self):

        """
        :return: nothing
        Prevent window crashes by accessing
        the event queue as the puzzle is
        being solved- then pump all events
        from the queue.

        This tells the OS know that the
        program is still running.
        """

        for event in pygame.event.get():

            # Allows the window to be dragged or closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                pygame.event.pump()

    def _check_newval_validity(self, row, col, val_to_test, puzzle):

        """
        :param row: the row index
        :param col: the column index
        :param val_to_test: the value to check and place in the puzzle
        :param puzzle: the puzzle in question
        :return: if the value val_to_test works in the given row/column position/indexes
        """

        # Checking row
        for i, tile in enumerate(puzzle[row]):
            if tile == val_to_test and col != i:
                return False

        # Checking col
        for i in range(len(puzzle)):
            if puzzle[i][col] == val_to_test and row != i:
                return False

        # Checking boxes
        box_spot_x = col // 3  # This will either give you a 0, 1 or 2
        box_spot_y = row // 3

        """
        Note that we need just the boxes positions. 
        Tile positions WITHIN THE BOX are determined below.
        """

        # Grabbing the start and end ranges
        row_start = box_spot_y * 3  # This gets us the *starting* index from the given box spot
        row_end = row_start + 3  # This gets us the specific index belonging to the column
        col_start = box_spot_x * 3
        col_end = col_start + 3

        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                if puzzle[r][c] == val_to_test and (r, c) != (row, col):
                    return False

        return True

    def _get_tile_position(self, puzzle):

        empty_tile = 0
        try:
            for row_pos, row in enumerate(puzzle):
                for col_pos, tile in enumerate(row):
                    if tile == empty_tile:
                        return row_pos, col_pos
        except RecursionError as re:
            print(f"Recursive error while iterating through:\n{re}\n{puzzle}")

        return None




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
