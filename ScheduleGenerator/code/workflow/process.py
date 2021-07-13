"""
Process Data
"""
from tools.helper import correct_grade9_crsid
from tools.xl import read_dframe
from workflow import xpcs

class PCS:
    def __init__(self, specs, db, xdata, varmap):
        self.shout = specs.shout['basic_process_steps']
        # data warning
        self.dwstr = "DATA WARNING!"
        # processing step shout
        self.done = "Processing step complete: "
        self.say_done = lambda p: print("{}{}".format(self.done, p))
        
        # process
        self.pcs_databank(specs, db, xdata)
        # xtra
        self.pcs_xtra(specs, db, xdata, varmap)
        # Sanity check
        self.sanity = True
        badstuds, freeps = self.check_sanity(db, xdata, specs.days)
        # Log
        self.print_log(specs, xdata, badstuds)

    def pcs_databank(self, specs, db, xdata):
        """Process data into databank structure"""
        steps = [
            ("Student", 'studs'),
            ("Teacher", 'faculty'),
            ("Section", 'sects'),
            ("Course", 'courses')
        ]
        self.pcs_base_steps(steps, db)
    
        more_steps = [
            ('stud_sect', 'stud_sects'),
            ('stud_course', 'stud_courses'),
            ('xcept', 'exceptions'),
        ]
        self.pcs_more_steps(more_steps, specs, db, xdata)
    
    def pcs_base_steps(self, steps, db):
        for cname, fname in steps:
            filename = db.fnames[fname]
            c = db.cls_list[db.cls_idx[cname]]
            db.pcs_step(c, fname=filename)
            if self.shout:
                print("Processed file {}...".format(filename))

    def pcs_more_steps(self, steps, specs, db, xdata):
        for step, name in steps:
            _, rows = read_dframe(db.fnames[step])
            step_call = getattr(self, "pcs_"+name)
            step_call(specs, db, xdata, rows)
            if self.shout: self.say_done(name)

    def pcs_xtra_steps(self, steps, db, xdata, varmap):
        for step, args in steps:
            step_call = getattr(self, "xpcs_"+step)
            step_call(db, xdata, varmap, *args)
            if self.shout: self.say_done(step)

    def pcs_xtra(self, specs, db, xdata, varmap):
        """All extra processing steps"""
        # for each grade cohort
        for g, cohort in xdata.grades.items():
            cohort.detect_bad_ids(db.students, specs)
            cohort.get_student_ids(db.students)
            cohort.clean_bad_ids(xdata.new_ids, specs.shout['bad_student_ids'])
            cohort.gender_count(db.students)
        # cleanup of bad student ids
        if specs.cleanup:
            xpcs.clean_student_ids(db.students, db.sections, xdata.new_ids, specs.shout['bad_student_ids'])
            xpcs.clean_cohort_ids(xdata.new_ids, xdata.grades, specs.id2grade)
            if self.shout: self.say_done("cleanup ids")
        # processing steps
        xtra_steps = [
            ("sects_detail", []),
            ("meetmap", [specs.mtm]),
            ("bands", [specs.bandbyid]),
            ("sections", [specs.shout['ignored_courses']]),
            ("teachers", [specs.btb]),
            ("grade_courses", []), # Deal with courses for parts of grade (not individuals)
            ("chunk_students", [specs.cap, specs.shout['chunk_students']])
            ("undecided", [specs.cap/2, specs.shout['undecided_listing']])
        ]
        self.pcs_xtra_steps(xtra_steps, db, xdata, varmap)

        # Special indices
        self.xpcs_special_idxs(xdata, varmap)
        # Conflicting sections
        xpcs.find_clash(db.students, xdata, varmap)

    def print_log(self, specs, xdata, badstuds):
        """ Report """
        if specs.shout['phase_completion']:
            print("\nPhase 2 complete.")
        if self.shout == 0: return

    """
    REST OF CODE HAS BEEN OMITTED!!
    """
    
    

