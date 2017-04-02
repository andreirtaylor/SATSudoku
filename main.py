#!/usr/bin/python2

import sys, os

def main(filename, ext=""):
    os.system("./sud2sat.py " + filename + " " + ext)

    os.remove("tmp")

if __name__ == '__main__':
    ## you must supply at least one argument
    if len(sys.argv) < 2:
        sys.stderr.write(usage)
        sys.exit(1)

    input_file = sys.argv[1]
    
    if len(sys.argv) < 3:
        main(input_file)
    else:
        ext = sys.argv[2]
        main(input_file, ext)
