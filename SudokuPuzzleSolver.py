# © 2020 Lawrence Chiappelli. All Rights Rerserved.
import os
import warnings
import copy
import re

class PuzzleInterface:

    def __init__(self):
        self.all_puzzle_files = [puzzlefile for puzzlefile in os.listdir('CSCI4463SudokuPuzzles') if puzzlefile.endswith(".txt")]

    def get_all_csci4463_puzzle_files(self):
        return self.all_puzzle_files

    def get_a_csci4463_puzzle_file(self, index):
        return self.all_puzzle_files[index]

    def get_csci4463_puzzle_difficulty(self, puzzlefile):

        easy_puzzles = ["01", "02", "06", "10", "13"]
        medium_puzzles = ["03", "04", "07", "11", "14"]
        hard_puzzles = ["05", "08", "09", "12", "15", "16"]

        file_difficulty = re.search(r'\d+', puzzlefile).group(0)
        if file_difficulty in easy_puzzles:
            return "Easy"
        elif file_difficulty in medium_puzzles:
            return "Medium"
        elif file_difficulty in hard_puzzles:
            return "Hard"
        else:
            warnings.warn("Unable to detect each file's difficulty based on the current working environment.", Warning)
            return "N/A - Could not determine difficulty"

    def read_puzzle_from_file(self, file):
        try:
            with open(f'CSCI4463SudokuPuzzles/{file}', 'r') as file_contents:
                puzzle = file_contents.read()
                return puzzle
        except FileNotFoundError as fnfe:
            warnings.warn(f"Files were not found:\n{fnfe}\n\nLast check for files- searching root directory...", UserWarning)
            with open(file, 'r') as puzzle:
                return puzzle

    def solve_puzzle_with_backtracking(self, puzzle):

        empty_tile = self._get_tile_position(puzzle)

        if empty_tile is None:
            return True
        else:
            row_pos, col_pos = empty_tile

        for test_val in range(1, 10):
            if self._check_newval_validity(row_pos, col_pos, test_val, puzzle):
                puzzle[row_pos][col_pos] = test_val

                if self.solve_puzzle_with_backtracking(puzzle):
                    return self.print_board_organized(puzzle)

                # Here, *RESET* the tile to 0 if the given solutions do not work. This is backtracking.
                puzzle[row_pos][col_pos] = 0

        return False

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

    def print_board_organized(self, puzzle):

        organized = ""
        for row in puzzle:
            organized += f"\n{row}"
        return organized

    def get_puzzle_as_2d_array(self, puzzle):

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
