import numpy as np

very_large_number = 999999999999999


class RDS:
    def __init__(self, n, inf, sup, c):
        """

        :param n: Number of variables
        :param inf: the minimum value of ??
        :param sup: the maximum value of ??
        :param c: constraints in a really cool form.
        """
        self.n = n
        self.assignment = np.zeros(n)  # initial assignment, this is used in dfbb # TODO: move it there
        self.temp_assignment = [-1] * n  # initial assignment, this is used in dfbb and lower-bound (needed here tho)
        self.rds = np.zeros(n + 1)  # the rds vector, the upper-bounds of each sub-problem
        self.inf = inf
        self.sup = sup
        self.C = c

    def dfbb(self, lbi, ubi, i):

        """
        This function is the classical depth-first branch-&-bound algorithm which
        we modified for our instances of interest.
        :param lbi: inital lower bound
        :param ubi: initial upper bound
        :param i: all variables indexed >= i are being branch-&-bound-ed
        :return: an upper bound for the partial assignment of values between i and n; F if fails to do such.
        """

        values = {
            'lb': self.inf,  # Modifiable LB
            'ub': ubi,  # Modifiable UB
            'v': i,  # start point for assigning
            's': False,  # Whether or not we have checked all the vars from i to n
            'current': 0  # Return value
        }  # Why? Since the outer variables were only to read inside not modify; But this way you can.

        def depth():
            """
            This function deepens to n. i.e moves across the depth of the tree.
            """
            if values['v'] == self.n:
                values['s'] = True
                values['ub'] = values['lb']
                self.assignment = self.temp_assignment
                if lbi < values['ub']:
                    width()
                else:
                    end()
            else:
                self.temp_assignment[values['v']] = self.sup - 1
                values['v'] = values['v'] + 1

        def width():
            """
            This function moves along the width of a certain level by checking possible
            values from the domain; Stops if reaches the final value for the domain.
            """
            if self.temp_assignment[values['v']] == 1:  # TODO: add domain value to class attributes
                values['v'] = values['v'] - 1
                if values['v'] == i:
                    end()
                else:
                    width()
            else:
                self.temp_assignment[values['v']] += 1
                values['lb'] = self.lower_bound(i, values['v'])
                if values['lb'] < values['ub']:
                    depth()
                else:
                    width()

        def end():
            if values['s']:
                values['current'] = values['ub']
            else:
                values['current'] = 'F'

        depth()
        return values['current']

    def rds_function(self, ubi):
        """
        The main function of RDS algorithm. Starting from the last variable, we run branch-&-bound so we
        have an proper upper bound. Then we use the previous upper bound as the lower bound for the next
        subproblem.
        :param ubi: initial upper bound
        :return: not sure
        """
        self.rds[self.n] = self.inf
        for i in range(self.n - 1, 0, -1):
            lbp = self.rds[i + 1]
            ubp = self.upper_bound(ubi, lbp, i)
            ub = self.dfbb(lbp, ubp, i)
            if ub != 'F':
                self.rds[i] = ub
            else:
                return 'Fail'
        return ub  # TODO: Referenced before assignment?? return the assignment or return nothing instead

    @staticmethod
    def upper_bound(ubi, lbp, i):
        # TODO: Change the definition
        return very_large_number

    @staticmethod
    def all_var_in_cons(constraint, assigned_vars):
        """
        This function makes a element-wise subtraction of the constraints (that has one var if its index-val is 1)
        and assigned variables so far (that var is assigned if its index-val is 1, as well). If ew result in an array
        containing a -1 value, it means the constraint did not have at least one var that is assigned.

        :param constraint: a constraint of size n which contains the variables with value other than 0.
        :param assigned_vars: an array indicating the assigned variables so far
        :return: True if the assigned variables is a subset to variables in the constraint
        """
        return np.any(np.subtract(constraint, assigned_vars) == -1)

    def lower_bound(self, i, v):
        """
        The original lower-bound function. Consists of backward-checking, forward-checking, and RDS value.
        :param i: variables i to v are assigned
        :param v: variables i to v are assigned
        :return: the lower bound to the partial assignment with one step ahead vision.
        """
        assigned_vars = np.array([1 if j in range(i, v) else 0 for j in range(self.n)])

        #  LB_bc
        #  We know which var is assigned; the we apply the given constraint on the partial assignment
        #  Note the way we calculated the violation. We made a element-wise product of the assignment
        #  and the constraint

        lb_bc = 0
        for c in self.C:
            if self.all_var_in_cons(c, assigned_vars):
                if not c['Result'][0](np.sum(np.multiply(np.array(c['Constraint']),
                                                         self.temp_assignment)), c['Result'][1]):
                    lb_bc += c['Valuation']

        # LB_fc
        # Now, we are looking for the constraints that can be violated one step ahead.
        lb_fc = 0
        for c in self.C:
            for vv in (list(set(range(self.n)) - set(range(i, v)))):  # vars that are not assigned
                tmp = assigned_vars
                tmp[vv] = 1  # assigning one more var
                if not self.all_var_in_cons(c, assigned_vars) and self.all_var_in_cons(c, tmp):
                    temp_temp_a = self.temp_assignment
                    temp_temp_a[vv] = 0   # first assign it to 0 - calculate the violation value  # TODO: all the domain
                    val_0 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0
                    temp_temp_a[vv] = 1  # first assign it to 1 - calculate the violation value
                    val_1 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0

                    lb_fc += min(val_0, val_1)

        # LB_rds
        lb_rds = self.rds[v]

        return lb_bc + lb_fc + lb_rds
