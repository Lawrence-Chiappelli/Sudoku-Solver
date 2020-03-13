# © 2020 Lawrence Chiappelli. All Rights Rerserved.
import os
import warnings


class PuzzleInterface:

    def __init__(self):
        self.all_puzzle_files = [puzzlefile for puzzlefile in os.listdir('CSCI4463SudokuPuzzles') if puzzlefile.endswith(".txt")]

    def get_all_csci4463_puzzle_files(self):
        return self.all_puzzle_files

    def get_a_csci4463_puzzle_file(self, index):
        return self.all_puzzle_files[index]

    def get_a_csci4463_puzzle_from_file(self, file):
        try:
            with open(f'CSCI4463SudokuPuzzles/{file}', 'r') as file_contents:
                puzzle = file_contents.read()
                return puzzle
        except FileNotFoundError as fnfe:
            warnings.warn(f"Files were not found:\n{fnfe}\n\nLast check for files- searching root directory...", UserWarning)
            with open(file, 'r') as puzzle:
                return puzzle

    def solve_puzzle_with_constraint_propagation(self, puzzle):

        if self._is_valid_board(puzzle):

            for number in puzzle:
                if number == 0:
                    self._assign_and_satisfy_constaint(puzzle, number)

            puzzle_solved = self._is_puzzle_solved(puzzle)
            if puzzle_solved:
                return puzzle
            else:
                return None

    def _is_valid_board(self, puzzle):

        counted_tiles = 0
        max_possible_tiles = 81

        for tile in puzzle:
            if str(tile).isdigit():
                counted_tiles += 1

        if counted_tiles != max_possible_tiles:
            raise AssertionError(f"Invalid Sudoku board detected, counted {counted_tiles}/{max_possible_tiles} possible tiles.")

    def _assign_and_satisfy_constaint(self, puzzle, number):
        new_number = None
        for new_number in range(1, 9):
            pass

        return new_number

    def _is_puzzle_solved(self, puzzle):
        if puzzle == puzzle:
            return False
        else:
            return True

    def _util_3(self, a, b):
        return a, b


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
