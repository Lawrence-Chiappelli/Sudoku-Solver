# © 2020 Lawrence Chiappelli. All Rights Rerserved.

import os


class PuzzleInterface:

    def __init__(self):
        self.all_puzzles = [puzzlefile for puzzlefile in os.listdir('CSCI4463SudokuPuzzles') if puzzlefile.endswith(".txt")]

    def get_puzzles(self):
        return self.all_puzzles

    def solve_puzzle_with_CSP_search_technique(self, puzz):

        goal_state = False
        if goal_state:
            return puzz
        else:
            return None


if __name__ == '__main__':

    puzzleinterface = PuzzleInterface()

    solved = None
    for puzzle in puzzleinterface.get_puzzles():

        solved = puzzleinterface.solve_puzzle_with_CSP_search_technique(puzzle)

        if solved:
            print(solved)
        else:
            print(f"Unable to solve puzzle: {puzzle}")


else:
    raise ModuleNotFoundError(f"Please set SudokuPuzzleSolver.py as the script path!")

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
