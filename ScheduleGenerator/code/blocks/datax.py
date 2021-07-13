"""
Data structures not part of the databank
"""
from tools.helper import set_def_props
from tools.grade import Grade

from collections import defaultdict

class DataX:
    # Number of teachers, sections, bands (set to 0)
    props_v = ['nteas', 'nsects', 'ns', 'nbds']

    # mt1_sects: Sections that can meet once per day
    # btb: Exceptions to the BTB limit rule
    # xs: Exceptions to individual schedule
    # clash: Conflicting sections
    props_l = ['mt1_sects', 'btb', 'xs', 'clash']
    
    # mts_sects: list of sections for each meet num
    # bands: sections for each band name
    # tea_sects: list of sections for each teacher
    # spots: sections size
    # tbd_courses: TBD courses
    # stud_crs_map: student-course map
    # stud_sects: student-sections map
    # chunked: set of chunked student ids
    props_d = ['new_ids', 'meetmap', 'mts_sects', 'bands', 'sect_names', 'tea_sects', 'spots', 'tbd_courses', 'stud_crs_map', 'stud_sects', 'chunk_weights', 'chunked', 'chunk_reps']
    
    def __init__(self, grades):
        # Default
        set_def_props(self, DataX.props_v, DataX.props_l, DataX.props_d)
        self.setup(grades)

    def setup(self, specs):
        """Initialize structures"""
        self.grades = {g : Grade(g) for g in specs.grades}
        # assignment to courses/sections
        self.decisions = defaultdict(list)
        # set of chunked student ids
        #self.chunked = set()
