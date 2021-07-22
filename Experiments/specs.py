"""
Object to maintain all system-wide parameters
"""

class Specs:
    def __init__(self):
        # Save
        self.fname = "dataset.csv"
        self.col_label = "revenue"
        self.col_group = "ticker"
        self.col_date = "date"
        self.chunk = 4
        self.analyze = False

