"""
Course data structure
"""
from blocks.block import Block

from config import DDAY
import numpy as np

PROPS = {
    "V": ["id", "name", "grade", "size", "dept",
          "meets", "band", "dday"],
    "L": ["sects"],
    "D": []
}

class Course(Block):
    @classmethod
    def pcs_input(cls, **kwargs):
        return super().pcs_input(**kwargs)
    
    @classmethod
    def pcs_row(cls, row):
        # process
        id = str(row.course_id)
        name = row.name.strip()
        # band
        if type(row.band) is float and np.isnan(row.band):
            bnd = "IGN"
        else:
            bnd = str(row.band)
        # grade
        if bnd == "IGN":
            grade = -1
        else:
            bnd = str(row.band)
            fc = id[0]
            if fc.isdigit():
                # Correction for 9th grade classes
                if fc != "1" and fc != "0":
                    id = "0" + id
                grade = int(id[0:2])
            elif fc == "C": # CADV
                grade = 12
            #else: #UADV
            #grade = int(id[-2:])
        try: size = int(row.size)
        except: size = 0
        dept = row.dept
        mts = row.meets
        if type(mts) is float:
            mts = "" if np.isnan(mts) else int(mts)
        meets = str(mts)
        band = "{}.{}".format(str(grade),bnd)
        dday = True if meets in DDAY else False
        # aggregate
        key, obj = cls.aggregate(id,name,grade,size,dept,
                                 meets,band,dday)
        return (key, obj)
