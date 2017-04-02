#!/usr/bin/python3

import sys, re, math

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
def base_convert(row, col, val, base):
    return int(base**2) * (row) + base * (col) + (int(val) - 1) + 1

# given a 0 indexed number from a base x base square return a unique representation of the
# row column and value
def ind_val_to_base(ind, val, base):
    i = ind // base
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
    for i in range(int(size**2)):
        row = []
        for val in range(size + 1):
            row.append(str(ind_val_to_base(i, val, size)))
        ret.append(" ".join(row))
    return ret

# generates the clauses for one number per entry
def once_per_row_clause(size):
    ret = []
    for row in range(size):
        # the values should be in the range of 1 -> 9
        for val in range(1, size + 1):
            for col1 in range(size):
                for col2 in range(size):
                    ret.append(" ")
    return ret

def sub_grid_clause(size):
    ret = []
    subgrid = int(math.sqrt(size))

    for k in range(1, size + 1):
        for a in range(subgrid):
            for b in range(subgrid):
                for u in range(1, subgrid + 1):
                    for v in range(1, subgrid):
                        for w in range((v + 1), subgrid + 1):
                            i  = 3*a + u
                            j1 = 3*b + v
                            j2 = 3*b + w
                            num1 = -base_convert(i-1, j1-1, k, size)
                            num2 = -base_convert(i-1, j2-1, k, size)
                            row = str(num1) + " " + str(num2)
                            ret.append(row)

    for k in range(1, size + 1):
        for a in range(subgrid):
            for b in range(subgrid):
                for u in range(1, subgrid):
                    for v in range(1, subgrid + 1):
                        for w in range((u + 1), subgrid + 1):
                            for t in range(1, subgrid + 1):
                                i1 = 3*a + u
                                j1 = 3*b + v
                                i2 = 3*a + w
                                j2 = 3*b + t
                                num1 = -base_convert(i1-1, j1-1, k, size)
                                num2 = -base_convert(i2-1, j2-1, k, size)
                                row = str(num1) + " " + str(num2)
                                ret.append(row)
    return ret


# Generates the list of rules for a size x size 
def generate_clauses(size):
    one_number = one_num_per_entry_clause(size)
    rows = once_per_row_clause(size)
    sub_grid = sub_grid_clause(size)

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
