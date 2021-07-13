"""
Run optimization with cvxpy
"""
import cvxpy
from cvxopt import glpk
import pickle
import math

from optim.variables import Variables
from optim.constraints import Constraints
from optim.objective import Objective

class SolverMIP:
    def __init__(self, specs, xdata):
        self.shout = specs.shout['optimization']
        self.slvr = specs.optimize['solver']
        self.savesol = specs.optimize['savesol']
        self.sol_fname = specs.make_srcfile(specs.optimize['fname'])
        if self.slvr == "LOAD":
            self.load()
        else:
            self.setup(specs, xdata, specs.optimize['ptype'])

    def setup(self, specs, xdata, ptype):
        """ Setup the optimization problem """
        # Set variables
        self.vars = Variables(specs, xdata)
        # Set constraints
        self.cons = Constraints(specs, self.vars, xdata)
        # Set cost
        self.objfun = Objective(specs, self.vars, self.cons, penal_type=ptype)
        # Save a copy
        #cst_copy = self.cons.copy()
        # Form objective.
        self.theobj = cvxpy.Minimize(self.objfun.cost)
        # Form problem.
        self.prob = cvxpy.Problem(self.theobj, self.cons.cs)
        # Shout
        if self.shout: print("Optim Setup complete...")

    def load(self):
        """Load from solution.pickle"""
        with open(self.sol_fname, 'rb') as f:
            self.prob, self.vars = pickle.load(f)

    def solve(self, time2run):
        """Run the solver"""
        # Options
        #glpk.options['obj_ll'] = 5.01
        #glpk.options['mip_gap'] = 0.1
        glpk.options['tm_lim'] = time2run

        # Solve
        if self.slvr == "LOAD":
            pass
        elif self.slvr == "GLPK":
            self.prob.solve(solver=cvxpy.GLPK_MI, verbose=self.shout)
        elif self.slvr == "GUROBI":
            self.prob.solve(solver=cvxpy.GUROBI, verbose=self.shout)

    def report(self):
        """Report solution"""
        val = self.prob.value
        tr = self.prob.solver_stats.solve_time
        print("SOLUTION Value: {}".format(val))
        if tr: print("Time: {} minutes".format(round(tr/60,2)))
        self.solved = False if math.isinf(val) else True
        if not self.solved:
            print("COULD NOT solve the problem, it is mathematically impossible to find a schedule that satisfies all constraints!")
 
    def save(self):
        """Write solution to file"""
        if not self.savesol: return
        with open(self.sol_fname, 'wb') as f:
            pickle.dump((self.prob, self.vars), f, pickle.HIGHEST_PROTOCOL)


