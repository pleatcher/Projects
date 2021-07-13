"""
Variables for optimization
"""
import cvxpy


class Variables:
    def __init__(self, specs, xdata):
        self.days = specs.days
        # Course-period, Teacher-period, objective
        self.cp = {}
        self.tp = {}
        self.sc = {}
        self.xscp = {}
        self.obj = None

        # Set
        self.set_vars(xdata.nteas, xdata.ns)
        self.set_vars2(xdata.stud_crs_map, xdata.tbd_courses)


    def set_vars(self, nteas, ns):
        """Create variables"""
        # Number of days
        ndays = len(self.days)
        # Teacher-day objective variable
        self.obj = cvxpy.Variable((nteas, ndays), integer=True)
        
        for day, nprds in self.days.items():
            self.cp[day] = cvxpy.Variable((ns, nprds), boolean=True)
            self.tp[day] = cvxpy.Variable((nteas, nprds), boolean=True)

    def set_vars2(self, stud_crs_map, tbd_courses):
        """Create student-section variables for PHASE 2"""
        # Student - courses (undecided)
        for stuid, crs_ids in sorted(stud_crs_map.items()):
            stu_map = {}
            vscp = {}
            for cid in crs_ids:
                ni = tbd_courses[cid][1]
                stu_map[cid] = cvxpy.Variable((ni,1),boolean=True)
                # xtra variables
                vscp[cid] = self.set_xtra(ni)
            
            self.xscp[stuid] = vscp
            self.sc[stuid] = stu_map

    def set_xtra(self, ni):
        """Create Vscp variables for PHASE 2
        We really want a constraint like this:
        Sum [Vsc * Vcp] = 1
        But solver won't allow so we convert into linear cstrts.
        We need to add new variables for every period.
        """
        weekset = {}
        # Every day
        for day, nprds in self.days.items():
            weekset[day] = cvxpy.Variable((ni,nprds),boolean=True)
        return weekset
