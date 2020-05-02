# Sudoku-Solver
This repository contains a downloadable (in-progress) application for solvable Sudoku puzzle challenges.

## Background

Originally a class assignment designed to solve predefined Sudoku challenges as a CSP (Constraint Satisfaction Problem), this application has been transformed into a GUI designed for the enjoyment of others. The algorithm used to solve a given Sudoku board is called "backtracking" (see SudokuPuzzleSolver.py).

In Artifical Intellgence, "backtracking is a general algorithm for finding all (or some) solutions to some computational problems, notably constraint satisfaction problems, that incrementally builds candidates to the solutions, and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution" - https://en.wikipedia.org/wiki/Backtracking

The implemented algorithm's accuracy has been verified by comparing its outputted solutions to various Sudoku solvers found online.

## Description

Puzzles included are those varying in difficulty provided by the professor as well as randomly generated ones. Click a tile to cycle through numbers 1-9. Right-click the same tile to cycle backwards.

Sudoku rules explained [here](https://www.bigfishgames.com/blog/how-to-solve-sudoku-puzzles-quickly-and-reliably/).

**TL;DR:**
* A Sudoku board consists of 9x9 tiles
* All numbers in each row must be unique
* All numbers in each column must be unique
* Diagnal numbers can be identical

## Download
The installer is available under [releases](https://github.com/Lawrence-Chiappelli/Sudoku-Solver/releases).

## Custom Compilation

1. `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz` onto your machine. I strongly recommend consulting outside resources to absolutely ensure that you are doing this correctly.
2. Change directories to the root of this repository.
3. Run the following magic line:

```
pyinstaller --onefile -w GUI.py
```

It will generate the .exe under the "dist" folder, so make sure to cut+paste it into the parent directory.

Just a fair warning- pyinstaller can be finicky. If using anaconda, install pyinstaller in the same anaconda virtual environment that you're using with this project.

Also note: include `--hidden-import "matplotlib` to the above command if you are contributing and using matplotlib. It behaves very strangely, which may be in part due to it's several dependencies on other libraries.

## Compatability

### Computer Specifications
Your computer requires very minimal processing power to run this application. 

However, there may be noticable lag when the program attempts to solve each puzzle *once*. As a vague benchmark: the easier puzzles takes roughly 1 second or less to solve on my PC. The hardest single puzzle takes about 5 seconds to solve. This area of performance should be considered moot nonetheless, as the algorithm is only run once and the duration may only last seconds.

### Operating System
* **Windows 10**: Tested and working
* **Linux**: Not tested
* **MacOS**: Not tested
