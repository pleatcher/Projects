"""
Student data structure
"""
from blocks.block import Block

PROPS = {
    "V": ["id", "first", "last", "name", "email", "grade", "gender", "xtime"],
    "L": ["sects", "courses"],
    "D": []
}

class Student(Block):
    @classmethod
    def pcs_input(cls, **kwargs):
        return super().pcs_input(**kwargs)
    
    @classmethod
    def pcs_row(cls, row):
        # process
        id = str(row.id)
        first = row.first.strip().title()
        last = row.last.strip().title()
        name = "{}. {}".format(first[0],last)
        email = row.email
        grade = int(row.grade)
        gender = row.gender
        xtime = False
        # aggregate
        key, obj = cls.aggregate(id, first, last, name, email, grade, gender, xtime)
        return (key, obj)
