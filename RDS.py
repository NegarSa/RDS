import numpy as np

very_large_number = 999999999999999


class RDS:
    def __init__(self, n, inf, sup, c):
        """
        :param n: Number of variables
        :param inf: the minimum value of result
        :param sup: the maximum value of result
        :param c: constraints in a really cool form.
        """
        self.n = n
        self.assignment = np.zeros(n)  # initial assignment
        self.temp_assignment = [-1] * n   # initial assignment, this is used in dfbb and lower-bound
        # TODO: (needed here tho?)
        self.rds = np.zeros(n + 1)  # the rds vector, the upper-bounds of each sub-problem
        self.inf = inf
        self.sup = sup
        self.C = c

    def dfbb(self, lbi, ubi, i):
        """
        This function is the classical depth-first branch-&-bound algorithm which
        we modified for our instances of interest.
        :param lbi: initial lower bound
        :param ubi: initial upper bound
        :param i: all variables indexed >= i are being branch-&-bound-ed
        :return: an upper bound for the partial assignment of values between i and n; F if fails to do such.
        """

        values = {
            'lb': self.inf,  # Modifiable LB
            'ub': ubi,  # Modifiable UB
            'v': i,  # start point for assigning
            's': False,  # Whether or not we have checked all the vars from i to n
            'current': 0,  # Return value
            'so_far': i
        }  # Why? Since the outer variables were only to read inside not modify; But this way you can.

        def depth():
            """
            This function deepens to n. i.e moves across the depth of the tree.
            """
            print('DEPTH')
            if values['v'] == self.n - 1:
                values['s'] = True
                values['ub'] = values['lb']
                self.assignment = self.temp_assignment
                print('All the variables have been assigned')
                print('S = True | Upper Bound Found: ' + str(values['ub']))
                print('Assignment: ', end='')
                print(self.assignment)
                if lbi < values['ub']:
                    print('Initial LB is less than the new upperbound')
                    width()
                else:
                    print('Upper Bound has surpassed the initial LB')
                    end()
            else:
                print('Current var is not the last one')
                print('Assignment valid from ' + str(i))
                print(self.temp_assignment)
                values['v'] = values['v'] + 1
                self.temp_assignment[values['v']] = -1
                print('v is now: ' + str(values['v']))
                if values['so_far'] != self.n:
                    values['so_far'] += 1
                width()

        def width():
            """
            This function moves along the width of a certain level
            by checking possible values from the domain;
            Stops if reaches the final value for the domain.
            """
            print('WIDTH')
            if self.temp_assignment[values['v']] == 1:
                # TODO: add domain value to class attributes
                print('reached the final value for the domain for variable: ' + str(values['v']))
                print('Rolling back')
                values['v'] = values['v'] - 1
                if values['v'] == i:
                    print('We have reached the final value for all variables from ' + str(i) + 'to ' + str(self.n))
                    end()
                else:
                    print('var ' + values['v'] + 'is not ')
                    width()
            else:
                print('Current Value of Var ' + str(values['v']) + ' :' + str(self.temp_assignment[values['v']]))
                self.temp_assignment[values['v']] += 1
                print('Moving to the next value for the :' + str(values['v']))
                print('Current Value of Var ' + str(values['v']) + ' :' + str(self.temp_assignment[values['v']]))
                values['lb'] = self.lower_bound(i, values['v'], values['so_far'])
                print('The lower bound from' + str(i) + ' to ' + str(values['so_far']))
                print('The assignment is: ', end='')
                print(self.temp_assignment)
                if values['lb'] < values['ub']:
                    print('The lower bound founded is less than the upper bound fixed.')
                    depth()
                else:
                    print('We have found a lower bound that is greater than the upper bound.')
                    width()

        def end():
            print('END:')
            if values['s']:
                print('Final achieved upper bound: ', end='')
                values['current'] = values['ub']
                print(values['ub'])
            else:
                print('Never achieved a fulfilling assignment yet made it to a exiting condition. i.e. Failure.')
                values['current'] = 'F'

        depth()
        return values['current']

    def rds_function(self, ubi):
        """
        The main function of RDS algorithm. Starting from the last variable,
        we on the partial sub-problem limited to i-n variables run branch-&-bound
        so we have an proper upper bound. Then we use the previous upper bound as
        the lower bound for the next sub-problem.
        :param ubi: initial upper bound
        :return: not sure
        """
        self.rds[self.n] = self.inf
        for i in range(self.n - 1, 0, -1):
            print('RDS main loop')
            print('i: ' + str(i))
            lbp = self.rds[i + 1]
            print('Lower Bound for this sub-problem: ' + str(lbp))
            ubp = self.upper_bound(ubi, lbp, i)
            print('The upper bound for this sub-problem: ' + str(ubp))
            ub = self.dfbb(lbp, ubp, i)
            print('BACK TO RDS')
            print('DFBB result: ' + str(ub))
            if ub != 'F':
                print('Saving this Upper Bound in RDS array')
                self.rds[i] = ub
                print(self.rds)
            else:
                print('FAILURE')
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
        return np.any(np.subtract(constraint['Constraint'], assigned_vars) == -1)

    def lower_bound(self, i, v, so_far):
        """
        The original lower-bound function. Consists of backward-checking, forward-checking, and RDS value.
        :param i: variables i to so_far are assigned
        :param v: variable currently being modified
        :param so_far: variables i to so_far are assigned
        :return: the lower bound to the partial assignment with one step ahead vision.
        """
        assigned_vars = np.array([1 if j in range(i, so_far) else 0 for j in range(self.n)])

        #  LB_bc
        #  We know which var is assigned; the we apply the given constraint on the partial assignment
        #  Note the way we calculated the violation. We made a element-wise product of the assignment
        #  and the constraint
        print('Assigned Variables: ', end='')
        print(assigned_vars)
        print("Calculating the backward checking lower-bound")
        lb_bc = 0
        for c in self.C:
            if self.all_var_in_cons(c, assigned_vars):
                print('This constraint involves a subset of variables in the partial assignment')
                print(c['Constraint'])
                if not c['Result'][0](np.sum(np.multiply(np.array(c['Constraint']),
                                                         self.temp_assignment)), c['Result'][1]):
                    lb_bc += c['Valuation']
                    print('LBBC :' + str(c['Valuation']))

        # LB_fc
        # Now, we are looking for the constraints that can be violated one step ahead.
        lb_fc = 0
        for c in self.C:
            for vv in (list(set(range(self.n)) - set(range(i, so_far)))):  # vars that are not assigned
                tmp = assigned_vars
                print('Variable ' + str(vv) + ' is not assigned yet.')
                tmp[vv] = 1  # assigning one more var

                if not self.all_var_in_cons(c, assigned_vars) and self.all_var_in_cons(c, tmp):
                    print('This constraint involves a subset of variables in the partial assignment now')
                    print(c['Constraint'])
                    temp_temp_a = self.temp_assignment
                    print('But what if we assign value 0 to it?')
                    temp_temp_a[vv] = 0   # first assign it to 0 - calculate the violation value  # TODO: all the domain
                    val_0 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0
                    print('It has the valuation of: ' + str(val_0))
                    print('But what if we assign value 0 to it?')
                    temp_temp_a[vv] = 1  # first assign it to 1 - calculate the violation value
                    val_1 = c['Valuation'] \
                        if not c['Result'][0](np.sum(np.multiply(
                                                     np.array(c['Constraint']), temp_temp_a)), c['Result'][1]) else 0
                    print('It has the valuation of: ' + str(val_0))
                    lb_fc += min(val_0, val_1)
                    print('Now we have our LBFC to:' + str(lb_fc))

        # LB_rds
        # Refer to the main paper for an explanation on this one
        lb_rds = self.rds[v]
        print('LB_RDS: ' + str(lb_rds))
        return lb_bc + lb_fc + lb_rds
