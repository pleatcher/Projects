"""
Run all phases of the schedule generator
"""
from config import TIME2RUN
from tools.helper import minute
from tools.specs import Specs
from blocks.databank import Databank
from blocks.datax import DataX
from optim.varmap import VariableMap
from workflow.process import PCS
from optim.solver import SolverMIP
from workflow.result import Result

import sys

def phase1(specs):
    db = Databank(specs)
    xdata = DataX(specs)
    return (db, xdata)

def phase2(specs, db, xdata):
    varmap = VariableMap()
    pc = PCS(specs, db, xdata, varmap)
    return varmap

def phase3(specs, xdata):
    solver = SolverMIP(specs, xdata)
    return solver

def phase4(solver, t2r):
    solver.solve(t2r)
    solver.report()
    if solver.solved: solver.save()

def phase5(specs, db, xdata, varmap, vars):
    res = Result(specs, db, xdata, varmap, vars)

def main(phases2run=0, t2r=TIME2RUN):
    # =============================================
    # Step 0: Prep
    # =============================================
    specs = Specs()
    
    # =============================================
    # Step 1: Read data, create db
    # =============================================
    db, xdata = phase1(specs)
    if phases2run == 1: return
    
    # =============================================
    # Step 2: Process databank
    # =============================================
    varmap = phase2(specs, db, xdata)
    if phases2run == 2: return

    # =============================================
    # Step 3: Setup optimization
    # =============================================
    solver = phase3(specs, xdata)
    if phases2run == 3: return
    
    # =============================================
    # Step 4: Run optimization
    # =============================================
    phase4(solver, t2r)
    if phases2run == 4 or not solver.solved: return
    
    # =============================================
    # Step 5: Generate schedules
    # =============================================
    phase5(specs, db, xdata, varmap, solver.vars)


if __name__== "__main__":
    # Default: option=0 i.e. run all
    opt_num = 0
    time_to_run = TIME2RUN
    if len(sys.argv) > 1:
        opt_num = int(sys.argv[1])
        if opt_num == 0:
            t2r = int(sys.argv[2])*minute
    # Run
    main(phases2run=opt_num,t2r=time_to_run)
