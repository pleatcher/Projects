"""
Databank structure
"""
from blocks.dbs import Dbase
import blocks.student as BK_student
import blocks.teacher as BK_teacher
import blocks.section as BK_section
import blocks.course as BK_course

PROPS = {
    "D": ["students", "teachers", "sections", "courses"]
}

BLK_LIST = [
    BK_student.Student,
    BK_teacher.Teacher,
    BK_section.Section,
    BK_course.Course
]

ALL_PROPS = {
    "Databank" : PROPS,
    "Student": BK_student.PROPS,
    "Teacher": BK_teacher.PROPS,
    "Section": BK_section.PROPS,
    "Course": BK_course.PROPS
}

class Databank(Dbase):
    
    def __init__(self, specs):
        # Initialize
        super().__init__(specs.files, specs.shout['read_data'])
        self.cls_list = BLK_LIST
        self.all_props = ALL_PROPS
        self.setup()
