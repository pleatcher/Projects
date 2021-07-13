"""
Maintain relevant data for one grade
"""
from collections import defaultdict

class Grade:
    def __init__(self, g):
        # grade integer
        self.g = g
        # list of sections
        self.sects = []
        # list of student ids
        self.stud_ids = []
        # list of student info
        self.stud_info = []
        # gender count
        self.gender = {'F':0,'M':0}
        # courses for entire grade
        self.courses = []
        # chunks of similar students
        self.chunks = {'F': defaultdict(list),'M': defaultdict(list)}
        # bad ids
        self.bad_ids = []

    def detect_bad_ids(self, students, specs):
        """Find all mismatched ids"""
        for sid, stud in students.items():
            if stud.grade != self.g: continue
            # grade from id
            id_grade = specs.id2grade(sid)
            # mismatch
            if id_grade != stud.grade:
                self.bad_ids.append(sid)

    def get_student_ids(self, students):
        """Create list of student ids for grade"""
        for sid, stud in students.items():
            if stud.grade != self.g or sid in self.bad_ids: continue
            self.stud_ids.append(sid)

    def clean_bad_ids(self, new_ids, shout):
        """find new ids for bad ids"""
        errstmt = "COULD NOT FIND BETTER ID for {} !!"
        m1,m2 = min(self.stud_ids),max(self.stud_ids)
        if shout: print("Student ID range: ", self.g, m1, m2)
        t1, tmax = int(m1), int(m2)
        for badid in self.bad_ids:
            while t1 < tmax:
                t1 += 1
                if t1 not in self.stud_ids:
                    new_ids[badid] = str(t1)
                    break
            if t1 == tmax:
                print(errstmt.format(badid))
            # Add to list now, delete later if necessary
            self.stud_ids.append(badid)

    def gender_count(self, students):
        """Count genders for grade"""
        for sid in self.stud_ids:
            self.gender[students[sid].gender] += 1
