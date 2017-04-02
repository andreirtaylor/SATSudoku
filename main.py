#!/usr/bin/python2

import sys, os

def main(filename):
    os.system("./sud2sat.py " +  filename)

    os.remove("tmp")

if __name__ == '__main__':
    ## you must supply at least one argument
    if len(sys.argv) < 2:
        sys.stderr.write(usage)
        sys.exit(1)

    input_file = sys.argv[1]

    main(input_file)
