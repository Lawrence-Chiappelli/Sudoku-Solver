import SudokuPuzzleSolver
import time

if __name__ == '__main__':

    puzzleinterface = SudokuPuzzleSolver.PuzzleInterface()
    all_puzzle_files = puzzleinterface.get_all_csci4463_puzzle_files()

    solved = None
    solved_counter = 0

    for index, file in enumerate(all_puzzle_files):

        puzzle = puzzleinterface.read_puzzle_from_file(file)
        puzzle = puzzleinterface.get_puzzle_as_2d_array(puzzle)
        difficulty = puzzleinterface.get_csci4463_puzzle_difficulty(file)
        print(f"Solving puzzle {index+1}/{len(all_puzzle_files)} | Difficulty: {difficulty} {puzzleinterface.print_board_organized(puzzle)}")

        before = time.perf_counter()
        solved = puzzleinterface.solve_puzzle_with_backtracking(puzzle)
        after = time.perf_counter()

        if solved:
            solved_counter += 1
            print(f"\nSolved puzzle {index+1}/{len(all_puzzle_files)} (elapsed time: {round(after-before, 3)} seconds):{solved}\n")
        else:
            print(f"WARNING: Could not solve above puzzle {file}")

    if solved_counter == len(all_puzzle_files):
        print(f"All {solved_counter} puzzles successfully solved in {round(time.perf_counter())} seconds! See above outputs.")
    else:
        print(f"{solved_counter}/{len(all_puzzle_files)} went unsolved. See above outputs.")


else:
    raise ModuleNotFoundError(f"Please set SudokuPuzzleSolver.py as the script path!")


