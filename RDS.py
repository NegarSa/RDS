import numpy as np


class RDS:
    def __init__(self, n, inf, sup, C):
        self.n = n
        self.assignment = np.zeros(n)
        self.temp_assignment = [-1] * n
        self.rds = np.zeres(n + 1)
        self.inf = inf
        self.sup = sup
        self.C = C

    def DFBB(self, lbi, ubi, i):
        lb = inf
        ub = ubi
        v = i
        s = False
        current = 0

        def depth():
            if v == n:
                s = True
                ub = lb
                self.assignment = self.temp_assignment
                if lbi < ub:
                    width()
                else:
                    end()

        def width():
            if A[v] == d:
                v = v - 1
                if v == i:
                    end()
                else:
                    width()
            else:
                self.temp_assignment[v] += 1
                lb = LowerBound(i, v)
                if lb < ub:
                    depth()
                else:
                    width()

        def end():
            if s:
                current = ub
            else:
                current = 'F'

        depth()
        return current

    def RDS(self, ubi):
        rds[self.n] = inf
        for i in range(n - 1, 0, -1):
            lbp = rds[i + 1]
            ubp = UPPERBOUND(ubi, lbp, i)
            ub = self.DFBB(lbp, ubp, i)
            if ub != 'F':
                rds[i] = ub
            else:
                return 'Fail'
        return ub

    def UPPERBOUND(ubi, lbp, i):
        # TODO: Change the definition
        return 99999999999

    def LowerBound(i, v):
        lb1 = 0

        def last_var_assigned(c):

            def c_includes_var(c, var):
                if c[var] == 1:
                    return True
                else:
                    return False

            for i in range(n, 1, -1):
                if c_includes_var(c, i):
                    continue
                else:
                    return i + 1
            return 1

        for c in self.C['Sum'].keys():
            if last_var_assigned(c) < v:
                r = 0
                for var in c[1:]:
                    if var == 1:
                        r = (r + var) % 2
                if r != c[0]:
                    lb1 += self.C['Sum'].get(c) 
            for c in self.C['More'].keys():
                r = 0
                for var in c[1:]:
                    if var == 1:
                        r = (r + A[var])
                if r < c[0]:
                    lb1 += self.C['More'].get(c)
        lb2 = 0
        lb3 = 0
        return lb1 + lb2 + lb3


c = {
    'Sum': {
        [0, 0, 1, 0, 0, 0, 0, 0, 0]: 1,
        [0, 1, 0, 0, 0, 0, 0, 0, 0]: 1,
        [0, 0, 0, 1, 0, 0, 0, 0, 0]: 1,
        [0, 0, 0, 0, 1, 0, 0, 0, 0]: 1,
        [0, 0, 0, 0, 0, 1, 0, 0, 0]: 1,
        [0, 0, 0, 0, 0, 0, 1, 0, 0]: 1,
        [0, 0, 0, 0, 0, 0, 0, 1, 0]: 1,
        [0, 0, 0, 0, 0, 0, 0, 0, 1]: 1,
        [0, 0, 0, 0, 0, 1, 1, 1, 1]: 99999999999,
        [0, 0, 1, 0, 1, 0, 1, 0, 1]: 99999999999,
        [0, 0, 0, 1, 1, 0, 0, 1, 1]: 99999999999,
        [0, 1, 1, 1, 1, 1, 1, 1, 1]: 99999999999,
    },
    'More': {
        [1, 1, 1, 1, 1, 1, 1, 1, 1]: 99999999999,
    }
}
