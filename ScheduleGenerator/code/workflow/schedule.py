"""
Extra Schedule processing methods
"""
import numpy

# ========================================================
# Subroutines
# ========================================================

"""

CODE HAS BEEN OMITTED!!
    
"""

def pcs_more_undecided(decisions, more_decisions, students):
    """ Yet more decisions """
    for cid, (stu_list,idxs,sects,imap) in more_decisions.items():
        enroll_by_gender(students, stu_list, sects, decisions, imap)

def enroll_by_gender(students, student_list, sects, decisions, imap):
    for vnum, inums in imap.items():
        ns = len(inums)
        thebin = 0
        for gender in 'FM':
            for stu_id, vi in student_list:
                if vi != vnum: continue
                if students[stu_id].gender != gender: continue
                loc = thebin % ns
                sect_id = sects[inums[loc]]
                decisions[stu_id].append([sect_id, vnum])
                thebin += 1

def get_rosters(decisions, students, rosters):
    """ Get roster per undecided section """
    for stuid, decs in decisions.items():
        gender = students[stuid].gender
        name = students[stuid].name
        for sid, idx in decs:
            entry = "{} {} {}".format(stuid, name, gender)
            rosters[sid]['r'].append(entry)
            rosters[sid][gender] += 1

def clean_band_name(name):
    """Remove digit from band name"""
    if name.endswith("1") and name[-2].isdigit() and name[-3].isalpha():
        return name[:-1]
    else:
        return name

def get_part(sid, name):
    """Get band name or section id"""
    if str(sid).isdigit(): # band
        part = clean_band_name(name)
    else: # section
        part = sid
    return part

def get_part_g(sid, name):
    """Get band name or section id for grade"""
    if str(sid).isdigit(): # band
        part = clean_band_name(name)
        part = part.split(".")[1]
    else: # section
        part = sid
    return part
