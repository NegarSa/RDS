# Alternative Formats for Representation:
## When the final decision is made, this will be the documentation to explain the formatting

```python
#1
C = {
    'Mod2': [
        {'Constraint': [0, 0, 0, 0, 0, 1, 1, 1, 1], 'Result': (operator.eq, 0)},
        {'Constraint': [0, 0, 1, 0, 1, 0, 1, 0, 1], 'Result': (operator.eq, 0)},
        {'Constraint': [0, 0, 0, 1, 1, 0, 0, 1, 1], 'Result': (operator.eq, 0)},
        {'Constraint': [0, 1, 1, 1, 1, 1, 1, 1, 1], 'Result': (operator.eq, 0)}
    ],
    'Mod10': [
        {'Constraint': [1, 1, 1, 1, 1, 1, 1, 1, 1], 'Result': (operator.ge, 1)}
    ]
}
OB = [1, 1, 1, 1, 1, 1, 1, 1]


#2

def op_eq_mod2(a, b):
    return a == (b % 2)


def op_ge_mod10(a, b):
    return a >= b



C = [
	{'Constraint': [1, 0, 0, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 1, 0, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 1, 0, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 1, 0, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 0, 1, 0, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 0, 0, 1, 0, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 0, 0, 0, 1, 0], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 0, 0, 0, 0, 1], 'Result': (op_eq_mod2, 0), 'Valuation': 1},
	{'Constraint': [0, 0, 0, 0, 1, 1, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
	{'Constraint': [0, 1, 0, 1, 0, 1, 0, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
	{'Constraint': [0, 0, 1, 1, 0, 0, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
	{'Constraint': [1, 1, 1, 1, 1, 1, 1, 1], 'Result': (op_eq_mod2, 0), 'Valuation': very_large_number},
	{'Constraint': [1, 1, 1, 1, 1, 1, 1, 1], 'Result': (op_ge_mod10, 1), 'Valuation': very_large_number},
]
```