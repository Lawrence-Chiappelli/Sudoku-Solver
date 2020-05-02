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
In-progress.

4/30/2020: As an alternative, download the repository as a ZIP (above). Then, open the dist directory and move GUI.exe into the root directory. The application should then, in theory, be launched successfully.

## Custom Compilation

1. `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz` onto your machine. I strongly recommend consulting outside resources to absolutely ensure that you are doing this correctly.
2. Change directories to the root of this repository.
3. Run the following magic line:

```
pyinstaller --hidden-import "matplotlib" --onefile GUI.py
```

My guess is that matplotlib is considered hidden because it's not being imported under GUI.py- the script that pyinstaller runs off of.

Just a fair warning- pyinstaller can be finicky. If using anaconda, install pyinstaller in the same anaconda virtual environment that you're using with this project.

## Compatability

### Computer Specifications
Your computer requires very minimal processing power to run this application.

### Operating System
This application been tested on Windows 10 only.