import SudokuPuzzleSolver
import time
import timeit

if __name__ == '__main__':

    puzzleinterface = SudokuPuzzleSolver.PuzzleInterface()
    all_puzzle_files = puzzleinterface.get_all_csci4463_puzzle_files()

    solved = None
    solved_counter = 0

    for index, file in enumerate(all_puzzle_files):

        puzzle = puzzleinterface.read_puzzle_from_file(file)
        puzzle = puzzleinterface.get_puzzle_as_2d_array(puzzle)

        print(f"Solving puzzle {index+1}/{len(all_puzzle_files)}:{puzzleinterface.print_board_organized(puzzle)}")

        elapsed = time.perf_counter()
        solved = puzzleinterface.solve_puzzle_with_backtracking(puzzle)

        if solved:
            solved_counter += 1
            print(f"\nSolved puzzle {index+1}/{len(all_puzzle_files)} (elapsed time: {elapsed} seconds):{solved}\n")
        else:
            pass

    if solved_counter == len(all_puzzle_files):
        print(f"All {solved_counter} puzzles successfully solved! See above outputs.")
    else:
        print(f"{solved_counter}/{len(all_puzzle_files)} went unsolved. See above outputs.")


else:
    raise ModuleNotFoundError(f"Please set SudokuPuzzleSolver.py as the script path!")


