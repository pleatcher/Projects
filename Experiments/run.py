import pandas as pd
import numpy as np

from specs import Specs
from process import pcs_data
from factory import ModelFactory


def main():
    my_specs = Specs()
    dataset = pcs_data(my_specs)
    
    #my_lab3 = ModelFactory(dataset, model="DRNN")
    #my_lab3.run_full()
    
    my_lab = ModelFactory(dataset, model="ARIMA")
    #my_lab.plot_labels()
    my_lab.run_full()
    
    my_lab2 = ModelFactory(dataset, model="SVR")
    my_lab2.run_full()

    results = ["\n{}\t{:.3}\t{:.3}".format(name, my_lab.test_err[name], my_lab2.test_err[name]) for name in dataset.keys()]
    print("\nMAPE comparison (not fair!) for: ARIMA/SVR/RNN")
    for line in results: print(line)
    print("\n\n")

if __name__== "__main__":
    main()
