# SATSudoku

This project solves sudoku puzzles as a boolean satisfiability problem 

It outputs statistics from minisat as well as the solved sudoku puzzle

```
output goes here
```

## Usage 

- Install [minisat](http://minisat.se/MiniSat.html) 
- Install [Python 2.7](https://www.python.org/download/releases/2.7/)
- Clone the repository
- Follow the desired instructions below

### Simple 9 x 9 Sudoku Problems

To run the sat solver on 9x9 sudoku puzzles run 

```
python main.py <input file>
```

#### Example 
```
python main.py samples/in_project_euler.txt
```

## Input Format

Input must come in the form of a text file containing encoded sudoku puzzles. 

All whitespace in the file is ignored and the puzzles contained withing are split into 81 character sets. 
Place a numeral for each value and any of the following for a null value `?.*0`.

Multiple puzzles can be encoded in the same file.

```
1638.5.7.
..8.4..65
..5..7..8
45..82.39
3.1....4.
7........
839.5....
6.42..59.
....93.81
```

This is equivalently represented by 

```
163805070
008040.650
    0500700845**820393010000407000000
        008390500006042005900???93081
```

## Contributors
| Name | Student Number|
| :----- | :---: |
| James Woo | V00816927 |
|Jake Cooper | V00794804 |
| Andrei Taylor | V00807046 |

## Know Issues
- Due to time constraints the projects only supported platform is Ubuntu 16.04
- Minisat produces a warning on some architectures regarding precision. This warning can be safely ignored
    - `WARNING: for repeatability, setting FPU to use double precision`
