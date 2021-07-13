""" This file contains default settings used throughout the project.
    These values can be configured by altering them below.
"""
from os import path
from tools.helper import minute, hour

################## PARAMETERS #######################
YEAR = 2021
GRADES = [9,10,11,12]
TIME2RUN = minute * 2

# Optimization
# 1 --> run the solver
# set to zero to load solution
SOLVE = 1

# Colors for output
# https://openpyxl.readthedocs.io/en/stable/styles.html
MY_COLORS = {
    'special': '00FF9900',
    9: '00FFCC99',
    10: '00CC99FF',
    11: '0099CCFF',
    12: '00FFFF00',
    'L' : 2, # red
    'F' : 7, # light blue
}

# Dimensions of cells for output
DIMENSIONS = { #col-width, row-height
    'bands_all': (12, 120),
    'bands_grade': (12, 100),
    'week': (20,20),
    'faculty': (30, 30),
    'students': (20, 20),
    'decisions': (22, 20),
}

# How much detail the system should report
# 0 = no noise
WHAT2REPORT = { # set to 1 if you want to report
    'read_data' : 0,
    'basic_process_steps' : 1,
    'bad_student_ids' : 0,
    'band_names' : 0,
    'band_listing' : 0,
    'ignored_courses' : 0,
    'chunk_students' : 1,
    'undecided_listing' : 1,
    'free_periods' : 0,
    'optimization' : 1,
    'output' : 1,
    'schedule_decisions' : 0,
    'phase_completion' : 0,
}

# Set to true if you want the system to replace bad student ids in output.
ID_CLEANUP = False #True


"""
CODE OMITTED HERE
""""

####################### Paths #######################
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

PATHS = {
    # Base
    'base': BASE_DIR,
    
    # Data files
    'data': path.join(BASE_DIR, 'data'),
    
    # Source files
    'source': path.join(BASE_DIR, 'source'),
    
    # output
    'output': path.join(BASE_DIR, 'output'),
}

####################### File Names ##################
FNAMES = {
    'faculty': "faculty",
    'studs': "students",
    'courses': "courses",
    'sects': "sections",
    'stud_sect': "students_sections",
    'stud_course': "students_courses",
    'xcept': "exceptions",
}

OUTNAMES = {
    'plan_faculty': "Faculty Schedule",
    'plan_students': "Students Schedule",
    'plan_bands': "Bands",
    'decisions': "Students Sections",
    'week': "Full Week"
}

EXT = "xlsx"

