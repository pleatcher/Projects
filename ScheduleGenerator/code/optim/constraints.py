"""
Set constraints for optimization problem with cvxpy
"""
import cvxpy

# --------------------------------------------
# Constraints
# --------------------------------------------
class Constraints:
    def __init__(self, specs, vars, xdata):
        # List of constraints
        self.cs = []
        # Adjustment for numeric errors
        self.adj = 0.0 #1e-01
        
        # Set all constraints
        self.set_constraints(specs, vars, xdata)

    def set_constraints(self, specs, vars, data):
        """ Main function: Set all constraints
            PHASE 1:
            obj: teacher-day objective variables

            cadv: M3 is senior college advisory period
            cpm: one section (course) meets per week
            1cpd: one section (course) meeting per day
            1cpt: one section (course) per teacher per period
            vlink: Teacher/period - section/period link
            tlunch: Teacher/period -- one lunch per day except F
            glunch: One lunch per day per grade except F
            btb: Teacher/period -- limit on consecutive periods
            
            PHASE 2:
            one: one section of course each (undecided) student
            :class size limit (capacity) each undecided student
            :the refactored * constraints on Vscp
        """
        # Type: course meetings per week
        self.add_cst_meets(vars.cp, data.meetmap, data.mts_sects, specs)
        # Only one 1st period per week
        self.add_cst_1pweek(vars.cp, 0, specs.daymarks)
        # Only one last period per week
        self.add_cst_1pweek(vars.cp, -1, specs.daymarks)
        # Teacher/period - exceptions
        self.add_cst_xs(vars.tp, data.xs, list(specs.daymarks))
        # at most two long days
        self.add_cst_longday(vars.tp, specs.long, specs.daymarks)
        # Special periods:
        self.add_cst_tr3(vars.cp)
        # Special constraints
        self.add_cst_special(vars.cp, vars.tp, data.special_idxs, specs)

        # ------------------------------------------
        for d, (day, nprds) in enumerate(specs.days.items()):
            # vars for day
            vtp = vars.tp[day]; vcp = vars.cp[day]
            vob = vars.obj[:,d]

            # ------------------------------------------
            # Type: one section (course) meeting per day
            self.add_cst_cpd(vcp, data.mt1_sects)
            # Student-period - one section, no clashes
            self.add_cst_clash(vcp, data.clash)
            # Teacher/period - limit consecutive periods to BTB
            self.add_cst_btb(vtp, nprds, data.btb)
            if day != 'F':
                # Teacher/period - at least one lunch free
                self.add_cst_tlunch(vtp, specs.lunch)
                # Lunch period for each grade
                self.add_cst_glunch(vcp, data.grades, specs.lunch)
            # ------------------------------------------

            # Iterate over teachers
            for t, (tea, idxs) in enumerate(data.tea_sects.items()):
                # Type: one section (course) per teacher per period
                self.add_cst_cpt(vcp, idxs)
                # Teacher/period - section/period link
                self.add_cst_vlink(vtp, vcp, t, idxs)
        # ------------------------------------------
        # Phase 2:
        # Type: one section of course each (undecided) student
        self.add_cst_onesect(vars.sc)
        # Type: class size limit (capacity) each undecided student
        self.add_cst_capacity(vars.sc, data.tbd_courses, data.spots, data.chunk_weights)
        # Type: the refactored * constraints on Vscp
        self.add_cst_xtra(vars, data.stud_crs_map, data.tbd_courses, data.stud_sects, specs.days)

    # --------------------------------------------
    # Individual Constraints
    # --------------------------------------------
    """
                
    REST OF THE CODE HAS BEEN OMITTED!!
        
    """


