import numpy as np

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

    def dfbb(self, lbi, ubi, i):
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

    def rds_function(self, ubi):
        self.rds[self.n] = self.inf
        for i in range(self.n - 1, 0, -1):
            lbp = self.rds[i + 1]
            ubp = self.upper_bound(ubi, lbp, i)
            ub = self.dfbb(lbp, ubp, i)
            if ub != 'F':
                self.rds[i] = ub
            else:
                return 'Fail'
        return ub

    @staticmethod
    def upper_bound(self, ubi, lbp, i):
        # TODO: Change the definition
        return very_large_number

    def lower_bound(self, i, v):
        # LB_bc
