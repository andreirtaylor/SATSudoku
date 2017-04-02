# SATSudoku

This project solves sudoku puzzles as a boolean satisfiability problem 

It outputs statistics from minisat as well as the solved sudoku puzzle

```
WARNING: for repeatability, setting FPU to use double precision
============================[ Problem Statistics ]=============================
|                                                                             |
|  Number of variables:           729                                         |
|  Number of clauses:            4007                                         |
|  Parse time:                   0.00 s                                       |
|  Eliminated clauses:           0.00 Mb                                      |
|  Simplification time:          0.00 s                                       |
|                                                                             |
============================[ Search Statistics ]==============================
| Conflicts |          ORIGINAL         |          LEARNT          | Progress |
|           |    Vars  Clauses Literals |    Limit  Clauses Lit/Cl |          |
===============================================================================
===============================================================================
restarts              : 1
conflicts             : 11             (inf /sec)
decisions             : 24             (0.00 % random) (inf /sec)
propagations          : 832            (inf /sec)
conflict literals     : 37             (0.00 % deleted)
Memory used           : 22.00 MB
CPU time              : 0 s

SATISFIABLE
3 5 1 | 2 8 6 | 4 9 7
4 9 2 | 1 5 7 | 6 3 8
7 8 6 | 9 3 4 | 5 1 2
------+-------+-------
2 7 5 | 4 6 9 | 1 8 3
9 3 8 | 5 2 1 | 7 6 4
6 1 4 | 8 7 3 | 2 5 9
------+-------+-------
8 2 9 | 6 4 5 | 3 7 1
1 6 3 | 7 9 2 | 8 4 5
5 4 7 | 3 1 8 | 9 2 6

Solved in 0.0150430202484 seconds.
```

## Usage 

- Install [minisat](http://minisat.se/MiniSat.html) 
- Install [Python 2.7](https://www.python.org/download/releases/2.7/)
- Clone the repository
- Follow the desired instructions below

### Simple 9 x 9 Sudoku Problems

To run the sat solver on 9x9 sudoku puzzles run 

```
python main.py <input file> [-e]
```

#### Example 
```
python main.py samples/in_project_euler.txt
```

### Extended Encoding

Additional constraints can be added using the -e flag 

The current additional constraints are
- There is at most one number in each entry

#### Example 

This will solve the problems in file `in_project_euler.txt` with the additional constraints.

```
python main.py samples/in_project_euler.txt -e
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
