"""
Helper functions
"""
# Fonts
from openpyxl.styles import colors, Font, Border, Side, Alignment,  PatternFill

#cell_BK = Font(color=colors.BLACK)
#cell_R = Font(color=colors.RED) #BLUE, BLACK, 99CC00green
#cell_G = Font(color= "99CC00") # Green
#cell_B = Font(color=colors.BLUE)
cell_fonts = {n: Font(color=colors.Color(indexed=n), size=14) for n in range(40)}
cell_fonts['B'] = Font(bold=True)
cell_fonts['BH'] = Font(bold=True, size=16)

thin = Side(border_style="thin")
double = Side(border_style="thick")
cell_align = {
    "C": Alignment(horizontal="center", vertical="center", wrapText=True),
    "CV": Alignment(vertical="center",wrapText=True)
}
cell_border = {
    "R": Border(right=double),
    "L": Border(left=double),
    "T": Border(top=double),
    "B": Border(bottom=double),
    "LT": Border(top=double, left=double),
    "RT": Border(top=double, right=double),
    "LB": Border(left=double, bottom=double),
    "RB": Border(right=double, bottom=double),
    "A": Border(top=double, left=double, right=double, bottom=double),
}

cell_fill = lambda c: PatternFill(start_color=c, end_color=c, fill_type="solid")

def get_cell_specs(font=None, fill=None, border=None, align=None):
    """Create dictinoary with cell specs"""
    specs = {}
    if font: specs['cell_font'] = cell_fonts[font]
    if fill: specs['cell_fill'] = cell_fill(fill)
    if border: specs['cell_border'] = cell_border[border]
    if align: specs['align'] = cell_align[align]
    return specs


# Time measures
second = 1000
minute = 60*second
hour = 60*minute

def set_def_props(self, props_v, props_l, props_d):
    """ Set default properties"""
    # Value props
    for p in props_v:
        setattr(self, p, 0)
    # List props
    for p in props_l:
        setattr(self, p, [])
    # Dict props
    for p in props_d:
        setattr(self, p, {})

def correct_grade9_crsid(course_id):
    """ Correction for 9th grade classes"""
    course_id = str(course_id)
    fc = course_id[0]
    if fc.isdigit() and fc != "1" and fc != "0":
        course_id = "0" + course_id
    return course_id
