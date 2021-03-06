from RDS import RDS

very_large_number = 999999999999999


def op_eq_mod2(a, b):
    return (a % 2) == b


def op_ge_mod10(a, b):
    return a >= b


C = [
    {'Constraint': [0, 1, 0, 0, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 1, 0, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 1, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 1, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 0, 1, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 0, 0, 1, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 0, 0, 0, 1, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 0, 0, 0, 0, 1], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
    {'Constraint': [0, 0, 0, 0, 0, 1, 1, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
    {'Constraint': [0, 0, 1, 0, 1, 0, 1, 0, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
    {'Constraint': [0, 0, 0, 1, 1, 0, 0, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
    {'Constraint': [0, 1, 1, 1, 1, 1, 1, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
    {'Constraint': [0, 1, 1, 1, 1, 1, 1, 1, 1], 'Result': (op_ge_mod10, 1), 'Valuation': very_large_number},
]

solve = RDS(8, 0, very_large_number, C)
print()
print("Final Value is: " + str(solve.rds_function(very_large_number, verbose=True)))
print("Best Assignment: " + str(solve.assignment))
