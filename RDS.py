import numpy as np
import operator

very_large_number = 999999999999999


class RDS:
    def __init__(self, n, inf, sup, C):
        self.n = n
        self.assignment = np.zeros(n)
        self.temp_assignment = [-1] * n
        self.rds = np.zeros(n + 1)
        self.inf = inf
        self.sup = sup
        self.C = C

    def DFBB(self, lbi, ubi, i):
        lb = self.inf
        ub = ubi
        v = i
        s = False
        current = 0

        def depth():
            if v == self.n:
                s = True
                ub = lb
                self.assignment = self.temp_assignment
                if lbi < ub:
                    width()
                else:
                    end()

        def width():
            if self.temp_assignment[v] == d:
                v = v - 1
                if v == i:
                    end()
                else:
                    width()
            else:
                self.temp_assignment[v] += 1
                lb = self.LowerBound(i, v)
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
        self.rds[self.n] = self.inf
        for i in range(self.n - 1, 0, -1):
            lbp = self.rds[i + 1]
            ubp = self.UPPERBOUND(ubi, lbp, i)
            ub = self.DFBB(lbp, ubp, i)
            if ub != 'F':
                self.rds[i] = ub
            else:
                return 'Fail'
        return ub

    def UPPERBOUND(self, ubi, lbp, i):
        # TODO: Change the definition
        return very_large_number

    def LowerBound(i, v):

        def last_var_assigned(c):

            def c_includes_var(c, var):
                if c['Constraint'][var] == 1:
                    return True
                else:
                    return False

            for i in range(n, 1, -1):
                if c_includes_var(c, i):
                    continue
                else:
                    return i + 1
            return 1

        def lbbc(A, c):
            if last_var_assigned(c['Constraint']) <= v:
                r = 0
                for var in c['Constraint']:
                    if var == 1:
                        r = (r + A[var])
                if c['Result'][0](r, c['Result'][1]):
                    return c['Valuation']
            else:
                return 0
        lb1 = 0
        for c in self.C:
            lb1 += lbbc(self.temp_assignment, c)

        lb2 = 0
        for c in self.C:
            lv = last_var_assigned(c['Constraint'])
            for v in range(0, lv):
                r = [0, 0]
                for i in [0, 1]:
                    A = self.temp_assignment
                    A[v] = i
                    r[i] += lbbc(A, c)
                lb2 += min(r[0], r[1])
                
        lb3 = self.rds[v]
        return lb1 + lb2 + lb3


