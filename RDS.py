import numpy as np

class RDS:
    def __init__(self, n, inf, sup, LowerB):
        self.n = n
        self.assignment = np.zeros(n)
        self.temp_assignment = np.zeros(n)
        self.rds = np.zeres(n + 1)
        self.inf = inf
        self.sup = sup
        self.LowerBound = LowerB
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
                if lbi < ub: width()
                else: end()
        def width():
            if A[v] == d:
                v = v - 1
                if v == i: end()
                else: width()
            else:
                self.temp_assignment[v] += 1
                lb = LowerBound(i, v)
                if lb < ub: depth()
                else: width()
        def end():
            if s: 
                current = ub
            else: 
                current = 'F'
        
        depth()
        return current
    def RDS(self, ubi):
        rds[self.n] = inf
        for i in range(n-1, 0, -1):
            lbp = rds[i + 1]
            ubp = UPPERBOUND(ubi, lbp, i)
            ub = self.DFBB(lbp, ubp, i)
            if ub != 'F':
                rds[i] = ub
            else:
                return 'Fail'
        return ub
    def UPPERBOUND(ubi, lbp, i):
        return 99999999999
        