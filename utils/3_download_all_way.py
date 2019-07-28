#!/usr/bin/env python

import csv
import subprocess


def run_main(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            if index > -1:
                if subprocess.call(['curl', row[1], '-o', str(index) + '.html']) != 0:
                    print('error: ' + str(index) + ' ' + row)
                    exit(1)


if __name__ == "__main__":
    run_main("list.csv")
