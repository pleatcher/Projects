import pandas as pd
import numpy as np

from specs import Specs
import process as pcs

def main():
    my_specs = Specs()
    dataset = pcs.pcs_data(my_specs)

if __name__== "__main__":
    main()
