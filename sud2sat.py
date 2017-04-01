#!/usr/bin/python

import sys, re

usage = """
python3 sat2sud <input_file> [output_file]

    input_file:
        the file to read from will not be changed by this program
    output_file: default = "sat_out.txt"
        place to write the output DIMACS formatted file
"""

# convert given a row,col (start at index 0) and a sudoku value start at 1
# convert the row, col and value into a unique base 9 number
# i.e. base_convert(0,0,1, 9) = 1
def base_convert(row,col,val, base):
    return base**2 * (row) + base * (col) + (int(val) - 1) + 1

# given a 0 indexed number from a base x base square return a unique representation of the
# row column and value
def ind_val_to_base(ind, val, base):
    i = ind / base
    j = ind % base
    return base_convert(i,j,val,base)

## given a valid sudoku file parse into a standard array of 81 character lines
def parse_into_standard_format(in_file, puzzle_lengh):
    ## create a single string from all the input
    longLine = "".join(["".join(x.strip().split()) for x in in_file.readlines() if "Grid" not in x])
    ## replace .?* with 0
    longLine = re.sub(r'[\.|\*|\?]', '0', longLine)
    ## now that the whole file is parsed return 81 character strings for each of the puzzles
    return [longLine[i:i+puzzle_lengh] for i in range(0, len(longLine), puzzle_lengh)]

# generates the clauses for one number per entry
def one_num_per_entry_clause(size):
    ret = []
    for i in range(size**2):
        row = []
        for val in range(size + 1):
            row.append(ind_val_to_base(i, val, size))
        print(row)
        ret.append(row)
    return ret

# Generates the list of rules for a size x size 
def generate_clauses(size):
    one_number = one_num_per_entry_clause(size)

## returns a list of sat encoded values for each of the non zero inputs in the file
def sat2sud(input_file):
    lines = []
    with open(input_file, 'r') as in_file:
        ## get 81 character lines in a standard format from the file (assuming 9x9 puzzle for now)
        lines = parse_into_standard_format(in_file, 81)
    ret = []
    for line in lines:
        for i in range(len(line)):
            if line[i] != '0':
                ret.append(ind_val_to_base(i, line[i],9))
    return ret

if __name__ == '__main__':
    ## you must supply at least one argument
    if len(sys.argv) < 2:
        sys.stderr.write(usage)
        sys.exit(1)

    input_file = sys.argv[1]
    sat = sat2sud(input_file)
    clauses = generate_clauses(9)
