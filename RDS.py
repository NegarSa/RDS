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
            else:
                self.temp_assignment[v] = self.sup - 1
                v = v + 1

        def width():
            if self.temp_assignment[v] == 1:
                v = v - 1
                if v == i:
                    end()
                else:
                    width()
            else:
                self.temp_assignment[v] += 1
                lb = self.lower_bound(i, v)
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
    def upper_bound( ubi, lbp, i):
        # TODO: Change the definition
        return very_large_number

    @staticmethod
    def all_var_in_cons( constraint, vars):
        return np.any(np.subtract(constraint, vars) == -1)

    def lower_bound(self, i, v):
        assigned_vars = np.array([1 if j in range(i, v) else 0 for j in range(self.n)])
        # LB_bc
        lb_bc = 0
        for c in self.C:
            if self.all_var_in_cons(c, assigned_vars):
                if not c['Result'][0](np.sum(np.multiply(np.array(c['Constraint']), self.temp_assignment)), c['Result'][1]):
                    lb_bc += c['Valuation']

        # LB_fc
        lb_fc = 0
        for c in self.C:
            for v in (list(set(range(self.n)) - set(range(i ,v)))):
                tmp = assigned_vars
                tmp[v] = 1
                if not self.all_var_in_cons(c, assigned_vars) and self.all_var_in_cons(c, tmp):
                    temp_temp_a = self.temp_assignment
                    temp_temp_a[v] = 0
                    val_0 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0
                    temp_temp_a[v] = 1
                    val_1 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0

                    lb_fc += min(val_0, val_1)

        # LB_rds
        lb_rds = self.rds[v]

        return lb_bc + lb_fc + lb_rds
