import numpy as np
import os
import random
from RDS import RDS


very_large_number = 999999999999999


def convert(filename):

    def op_eq_mod2(a, b):
        return (a % 2) == b

    file = open(filename)
    lines_list = file.readlines()
    cons = [[int(val) for val in line.split()] for line in lines_list]
    n = max([max(line) for line in cons])
    C = []
    for line in cons:
        c = {}
        t = list(np.zeros(n + 1))
        for e in line:
            t[e] = 1
        c['Constraint'] = t
        c['Result'] = (op_eq_mod2, 0)
        c['Valuation'] = very_large_number
        C.append(c)
    file.close()
    for i in range(n):
        c = {}
        t = list(np.zeros(n + 1))
        t[i + 1] = 1
        c['Constraint'] = t
        c['Valuation'] = 1
        if(random.random() > 0.6):
            c['Result'] = (op_eq_mod2, 0)
        else:
            c['Result'] = (op_eq_mod2, 1)
        C.append(c)
    return n, C


if __name__ == '__main__':
    n, C = convert(os.path.join('inputs', 'INPUT_FILE (1).txt'))
    solve = RDS(n, 0, very_large_number, C)
    print()
    print("Final Value is: " + str(solve.rds_function(very_large_number)))
    print("Best Assignment: " + str(solve.assignment))
