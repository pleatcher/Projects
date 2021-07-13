"""
Teacher data structure
"""
from blocks.block import Block

PROPS = {
    "V": ["id", "first", "last", "title", "name", "email", "btb"],
    "L": ["sects", "xs"],
    "D": []
}

class Teacher(Block):
    @classmethod
    def pcs_input(cls, **kwargs):
        return super().pcs_input(**kwargs)
    
    @classmethod
    def pcs_row(cls, row):
        # process
        id = row.id
        first = row.first_name.strip().title()
        last = row.last_name.strip().title()
        title = row.title.strip()
        name = "{} {}".format(title,last)
        email = row.email
        btb = 0
        # aggregate
        key, obj = cls.aggregate(id, first, last, title, name, email, btb)
        return (key, obj)
