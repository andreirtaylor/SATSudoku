#!/usr/bin/python2

import sys
import string
import math

N = 9

def display(puzzle, N):
    s = int(math.sqrt(N))
    squares = [s*(x+1) for x in range(s)]

    for idx, line in enumerate(puzzle):
        if (idx in squares):
            print('------+-------+-------\n'),
        for jdx, num in enumerate(line):
            if (jdx in squares):
                print('|'),
            print(str(num)),
        print

def sat2sud(input):
    with open(input, 'r') as sat:
        variables = []
        next(sat)

        '''
        N*N*N propositional variables.
        for each entry in the NxN grid S, we associate N variables
        s_xyz is assigned true iff the entry in row x and col y is assigned number z
        example: s_483 = 1 means that s[4,8] = 3

        here we are loading all positive values from the sat file into an array
        '''
        for line in sat:
            l = line.split()
            for i in l:
                if int(i) > 0:
                    variables.append(int(i))

        '''
        a puzzle that is N x N
        '''
        puzzle = [[0 for x in range(N)] for y in range(N)]

        '''
        continuously divide the variable to get where the number is
        since the variables start at 1, we subtract 1 to get the correct index
        the number is also indexed started from 0, so we add 1
        '''
        for v in variables:
            v, num = divmod(v-1, N)
            v, col = divmod(v, N)
            v, row = divmod(v, N)

            puzzle[row][col] = num + 1

        display(puzzle, N)

def main():
    if len(sys.argv) < 2:
        print('Too few arguments.')
        print('Usage:\n  sat2sud.py <INPUT>')
        print('sud2sat reads a Sudoku puzzle and converts it to CNF for miniSAT')
        print('  Input: input miniSAT file')
        sys.exit(-1)

    else:
        sat2sud(sys.argv[1])

if __name__ == "__main__":
    main()
