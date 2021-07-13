"""
Extra Data processing methods
"""
from collections import defaultdict

# ========================================================
# STUDENT IDS
# ========================================================
def clean_student_ids(students, sections, new_ids, shout):
    """Replace student objects with new keys"""
    line = "SWITCH: OLD: {}\tNew ID: {}"
    for bad_id, new_id in new_ids.items():
        if shout: print(line.format(bad_id,new_id))
        # Replace student with new id
        students[new_id] = students[bad_id]
        del students[bad_id]
        # Replace stuid in sections
        for sid in students[new_id].sects:
            sections[sid].stud_ids.remove(bad_id)
            sections[sid].stud_ids.append(new_id)

def clean_cohort_ids(new_ids, cohorts, id2grade):
    for bad_id, new_id in new_ids.items():
        # Add new ids to cohorts
        g = id2grade(new_id)
        if bad_id in cohorts[g].stud_ids:
            cohorts[g].stud_ids.remove(bad_id)
        cohorts[g].stud_ids.append(new_id)

# ========================================================
# BANDS
# ========================================================
def create_ibands(courses):
    # Course/section bands
    bandkeys = set(course.band for course in courses.values())
    # Ideal bands -- does not consider conflicts
    idealbands = {k:[] for k in bandkeys}
    for cid, course in courses.items():
        idealbands[course.band].extend(course.sects)
    #print(bandkeys, idealbands)
    return idealbands

def create_mixbands(sids):
    """Create bands by first digit of section num"""
    nb = set(sid[-2] for sid in sids)
    bands = {k:[] for k in sorted(nb)}
    for sid in sids:
        num = sid[-2]
        bands[num].append(sid)
    return list(bands.values())

def create_bands(sections, sids):
    """Takes section ids and creates bands recursively"""
    def _create(sids):
        theband = {}
        outband = []
        stuset = set()
        for sid in sids:
            tid = sections[sid].teacher_id
            studs = sections[sid].stud_ids
            if tid in theband or stuset.intersection(studs):
                outband.append(sid)
            else:
                stuset.update(studs)
                theband[tid] = sid
        return (list(theband.values()), outband)
        
    bands = []
    while sids:
        band, sids = _create(sids)
        bands.append(band)
    return bands

# ========================================================
# Exceptions
# ========================================================
def teacher_xs(teachers, row):
    """ Process teacher exceptions"""
    tid = row.id
    teachers[tid].btb = int(row.btb)
    if row.x == "none": return
    xlist = row.x.split(',')
    for x in xlist:
        d,p = split_xs(x.strip())
        teachers[tid].xs.append([d,p])

def split_xs(x):
    """Auxiliary function"""
    ds, ps = x.split('.')
    if '-' in ds:
        d = ds.split('-')
    else:
        d = (ds, ds)
    if '-' in ps:
        p = ps.split('-')
    else:
        p = (ps, ps)
    return (d,p)

# ========================================================
# MORE
# ========================================================
# Conflicting sections
def find_clash(students, xdata, varmap):
    clash = [set() for _ in range(xdata.ns)]
    for stuid, stud in students.items():
        # Set of sections for stud
        vs = varmap.sect2var
        idxs = [vs[sid] for sid in stud.sects if sid in vs]
        if not idxs: continue
        xdata.grades[stud.grade].stud_info.append([stuid, stud.name, idxs])
        for idx in idxs: clash[idx].update(idxs)
    # remove self section
    for n,vec in enumerate(clash):
        if n in vec: vec.remove(n)
    xdata.clash = [list(vec) for vec in clash]
    #print(xdata.clash)

def get_id_varset(all_ids, varmap):
    """Find the set of variables for al sections/courses"""
    idxs = set()
    for sid in all_ids:
        if sid in varmap.sect2var:
            vnum = varmap.sect2var[sid]
        elif sid in varmap.sect2band:
            vnum = varmap.band2var[varmap.sect2band[sid]]
        idxs.add(vnum)
    return idxs

def find_chunks(cohort, students, varmap):
    """Find groups of students by their common sect/band variables"""
    for stuid in cohort.stud_ids:
        stud = students[stuid]
        # Set of indixes for stud
        idxs = get_id_varset(stud.sects + stud.courses, varmap)
        cohort.chunks[stud.gender][frozenset(idxs)].append(stuid)


def calc_distance_mtx(students, varmap, grade, gender):
    """Calculate distance matrix for each pair of students
        in a given grade, with given gender
    """
    # Build matrix with sect/band variables
    ids, idx_mtx = [], []
    for stuid, stud in students.items():
        if stud.grade != grade or stud.gender not in gender: continue
        # Set of indixes for stud
        idxs = get_id_varset(stud.sects, varmap)
        idx_mtx.append(idxs)
        ids.append(stuid)
    n = len(idx_mtx)
    sizes = [len(vec) for vec in idx_mtx]
    best = max(sizes)
    # Create distance matrix (close => 0...1 <= far)
    dist_mtx = [[round(1 - len(idx_mtx[i].intersection(idx_mtx[j]))/max(1,sizes[i], sizes[j]),2) for j in range(n)] for i in range(n)]
    return (ids, dist_mtx)

"""
    ids, dist_mtx = xpcs.calc_distance_mtx(db.students, varmap, 11, 'M')
    from collections import Counter
    from sklearn.cluster import AgglomerativeClustering
    groups = AgglomerativeClustering(affinity='precomputed', n_clusters=6, linkage='complete').fit(dist_mtx)
    counts= Counter(groups.labels_)
    print(counts)
"""

# ========================================================
# Undecided courses
# ========================================================
def enroll_by_gender_course(students, grade, cid, gender='FM', skip=0, skiprule=None):
    tally = 0
    for stu_id, stud in students.items():
        if stud.grade != grade or stud.gender != gender: continue
        if skiprule and skiprule(stud): continue
        tally += 1
        if skip and 2-(tally % 2) == skip: continue
        students[stu_id].courses.append(cid)


def enroll_by_gender_random(sections, students, grade, sects, decisions, gender='FM', skip=0, skiprule=None):
    ns = len(sects)
    tally, thebin = 0, 0
    for stu_id, stud in students.items():
        if stud.grade != grade or stud.gender != gender: continue
        if skiprule and skiprule(stud): continue
        tally += 1
        if skip and 2-(tally % 2) == skip: continue
        sect_id = sects[thebin % ns]
        sections[sect_id].stud_ids.append(stu_id)
        students[stu_id].sects.append(sect_id)
        # Add to decisions
        decisions[stu_id].append([sect_id,thebin])
        thebin += 1


"""
    
REST OF CODE HAS BEEN OMITTED!!

"""
