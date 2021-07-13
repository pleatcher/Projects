"""
Set objective for optimization problem with cvxpy
"""
import cvxpy


# Objective function
# --------------------------------------------
class Objective:
    def __init__(self, specs, vars, cons, penal_type=0):
        # Penalty type, 0 = basic
        self.ptype = penal_type
        # add objective constraints
        self.add_csts(specs.days, vars, cons)
        # cost function
        self.cost = cvxpy.sum(vars.obj)

    def add_csts(self, days, vars, cons):
        """ Add consrtaints for objective """
        for d, (day, nprds) in enumerate(days.items()):
            # vars for day
            vtp = vars.tp[day]; vob = vars.obj[:,d]
            # Early/Mid/Late
            early, late, mid, whole = self.day_cost(vtp, nprds)
            # Weighted penalty
            penalty = self.day_penalty(early, late, mid)
            # Teacher-day (objective) variables
            cons.add_cst_obj(vob, penalty)

    def day_cost(self, vtp, nprds):
        """ Cost per day -- all teachers"""
        early = cvxpy.max(vtp[:,0:2], axis=1)
        late = cvxpy.max(vtp[:,nprds-2:nprds], axis=1)
        mid = cvxpy.max(vtp[:,2:nprds-2], axis=1)
        whole = cvxpy.max(vtp, axis=1)
        return (early, late, mid, whole)

    def day_penalty(self, early, late, mid):
        if self.ptype == 3:
            long = cvxpy.pos(early + late - 1.0)
            penalty = 2*early + mid + 2.0*late + 2.0*long
        elif self.ptype == 2:
            penalty = 2.0*early + mid + 2.0*late
        elif self.ptype == 1:
            penalty = early + late
        else:
            penalty = 1
        return penalty
