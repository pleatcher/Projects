"""
Section data structure
"""
from blocks.block import Block
from tools.helper import correct_grade9_crsid

PROPS = {
    "V": ["id", "course_id", "teacher_id", "term1","term2", "grade", "size"],
    "L": ["stud_ids"],
    "D": []
}

class Section(Block):
    @classmethod
    def pcs_input(cls, **kwargs):
        return super().pcs_input(**kwargs)
    
    @classmethod
    def pcs_row(cls, row):
        # process
        #id = row.section_id.strip()
        #course_id = id.split('-')[0]
        # Correction for 9th grade classes
        course_id = correct_grade9_crsid(row.course_id)
        id = "{}-{}".format(course_id,row.section_num)
        teacher_id = row.teacher_id
        term1 = True if row.term1 == "Y" else False
        term2 = True if row.term2 == "Y" else False
        grade = -1
        size = 0

        # aggregate
        key, obj = cls.aggregate(id, course_id, teacher_id, term1, term2, grade, size)
        return (key, obj)
