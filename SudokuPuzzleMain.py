import SudokuPuzzleSolver

if __name__ == '__main__':

    puzzleinterface = SudokuPuzzleSolver.PuzzleInterface()

    solved = None
    for index, file in enumerate(puzzleinterface.get_all_csci4463_puzzle_files()):

        puzzle = puzzleinterface.get_a_csci4463_puzzle_from_file(file)
        solved = puzzleinterface.solve_puzzle_with_constraint_propagation(puzzle)

        if solved:
            print(f"Puzzle {puzzleinterface.get_all_csci4463_puzzle_files()[index]} solved!\n\tORIGINAL:\n{puzzle}\n\n\tSOLVED:\n{solved}")
        else:
            print(f"Unable to solve puzzle: {puzzleinterface.get_all_csci4463_puzzle_files()[index]}")


else:
    raise ModuleNotFoundError(f"Please set SudokuPuzzleSolver.py as the script path!")
