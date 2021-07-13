"""
Object to maintain all system-wide parameters
"""
from config import *

class Specs:
    def __init__(self):
        # Save
        self.shout = WHAT2REPORT
        self.colors = MY_COLORS
        self.shape = DIMENSIONS
        self.days = DAYS
        self.grades = GRADES
        self.lunch = LUNCH
        self.long = LONGDAYS
        self.btb = BTB
        self.cap = CAP
        self.mtm = MEETMAP
        self.dday = DDAY
        self.orday = ORDAY
        self.cleanup = ID_CLEANUP
        self.bandbyid = MIXBANDS
        self.optimize = {
            'ptype': 0,     # penalty type
            'fname': "solution",  # name of solution file
            'savesol': True, # save solution variables to file?
            'solver' : "GUROBI" #"GLPK"
        }
        if not SOLVE:
            self.optimize['solver'] = "LOAD"

        
        # More useful parameters
        self.id2grade = lambda sid: 12 - (2000 + int(sid[1:3]) - YEAR - 1)
        
        self.daymarks = "".join(DAYS.keys())
        self.dayprds = DAYS.values()

        # File name helpers
        self.outnames = OUTNAMES
        self.make_fname = lambda folder,key: "{}/{}_{}.{}".format(PATHS[folder],FNAMES.get(key, key),YEAR,EXT)

        self.make_srcfile = lambda name: "{}/{}.{}".format(PATHS['source'],name,"pickle")

        self.make_outfile = lambda name: "{}/{}.{}".format(PATHS['output'],name,EXT)

        self.files = {key: self.make_fname('data', key) for key in FNAMES.keys()}

