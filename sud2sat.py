#!/usr/bin/python3

import sys, re, math, os, time, subprocess

N = 9

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
    #ret.append("c one number per entry")
    for i in range(int(size**2)):
        row = []
        for val in range(1, size + 1):
            row.append(str(ind_val_to_base(i, val, size)))
        ret.append(" ".join(row))
    return ret

def once_per_row_clause(size):
    ret = []
    #ret.append("c once per row")
    for col in range(size - 1):
        # the values should be in the range of 1 -> 9
        for val in range(1, size + 1):
            for row1 in range(size):
                for row2 in range(row1 +1, size):
                    values = str(-base_convert(row1, col, val, size)) + " " + str(-base_convert(row2, col, val, size))
                    ret.append(values)
    return ret

def once_per_column_clause(size):
    ret = []
    #ret.append("c once per column")
    for row in range(size):
        # the values should be in the range of 1 -> 9
        for val in range(1, size + 1):
            for col1 in range(size - 1):
                for col2 in range(col1 +1, size):
                    values = str(-base_convert(row, col1, val, size)) + " " + str(-base_convert(row, col2, val, size))
                    ret.append(values)

    return ret

def sub_grid_clause(size):
    ret = []
    #ret.append("c sub_grid1")
    subgrid = int(math.sqrt(size))

    for k in range(1, size + 1):
        for a in range(subgrid):
            for b in range(subgrid):
                for u in range(1, subgrid + 1):
                    for v in range(1, subgrid):
                        for w in range((v + 1), subgrid + 1):
                            i  = subgrid*a + u
                            j1 = subgrid*b + v
                            j2 = subgrid*b + w
                            num1 = -base_convert(i-1, j1-1, k, size)
                            num2 = -base_convert(i-1, j2-1, k, size)
                            row = str(num1) + " " + str(num2)
                            ret.append(row)
    #ret.append("c sub_grid2")
    for k in range(1, size + 1):
        for a in range(subgrid):
            for b in range(subgrid):
                for u in range(1, subgrid):
                    for v in range(1, subgrid + 1):
                        for w in range((u + 1), subgrid + 1):
                            for t in range(1, subgrid + 1):
                                i1 = subgrid*a + u
                                j1 = subgrid*b + v
                                i2 = subgrid*a + w
                                j2 = subgrid*b + t
                                num1 = -base_convert(i1-1, j1-1, k, size)
                                num2 = -base_convert(i2-1, j2-1, k, size)
                                row = str(num1) + " " + str(num2)
                                ret.append(row)
    return ret

# Generates the list of rules for a size x size
def generate_clauses(size):
    one_number = one_num_per_entry_clause(size)
    rows = once_per_row_clause(size)
    cols = once_per_column_clause(size)
    sub_grid = sub_grid_clause(size)

    return one_number + cols + rows + sub_grid

## returns a list of sat encoded values for each of the non zero inputs in the file
def sat2sud(input_file):
    lines = []
    with open(input_file, 'r') as in_file:
        ## get N*N character lines in a standard format from the file (assuming 9x9 puzzle for now)
        lines = parse_into_standard_format(in_file, N**2)
    ret = []
    for line in lines:
        tmp = []
        for i in range(len(line)):
            if line[i] != '0':
                tmp.append(str(ind_val_to_base(i, line[i], N)))
        ret.append(tmp)
    return ret

def print_stats(sat_cases):
    # create a temp file for output
    clauses = generate_clauses(N)
    output_file = "sudoku.cnf"
    results = "results.csv"
    times = []
    with open(results, 'w') as res:
        for idx, case in enumerate(sat_cases):

            startTime = time.time()
            
            with open(output_file, 'w') as out_file:
                out_file.write('p cnf ' + str(N**3) + ' ' + str((len(clauses) + len(case))) + '\n')
                for line in case:
                    out_file.write(line + " 0\n")
                for line in clauses:
                    out_file.write(line + " 0\n")
            
            # write to a random temp file
            os.system("minisat " +  output_file + "  " + "tmp")

            proc = subprocess.Popen("./sat2sud.py tmp", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            
            out = re.sub('[-+|\\n ]', '', out)

            t = time.time() - startTime
            times.append(t)
            res.write(str(idx + 1) + "," + str(t) + "," + out + "\n")

        res.write(str(reduce(lambda x, y: x + y, times) / len(times)))

if __name__ == '__main__':
    ## you must supply at least one argument
    if len(sys.argv) < 2:
        sys.stderr.write(usage)
        sys.exit(1)

    input_file = sys.argv[1]


    sat_cases = sat2sud(input_file)

    print_stats(sat_cases)

