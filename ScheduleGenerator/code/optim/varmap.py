"""
Variable map structure
to translate data into variables for optimization
"""

class VariableMap:
    def __init__(self):
        # Maps
        # section_id --> band_name
        # band_name --> variable number (idx)
        self.sect2band = {}
        self.band2var = {}
        self.var2band = {}
        
        # section_id --> variable number (idx)
        self.sect2var = {}
        self.var2sect = {}

        # teacher_id --> variable number among teas (idx)
        # section_id --> teacher_id
        self.sect2tea = {}
        self.tea2var = {}

