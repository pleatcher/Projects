import pandas as pd
import numpy as np

def pcs_data(specs):
    """Process dataset"""
    # read
    df = pd.read_csv(specs.fname)
    # clean up column names
    df.columns = [col.lower().replace(specs.prefix,"").replace(" ","_") for col in df]
    
    # Set of tickers
    #names = df[col_group].unique()
    # Get groups
    data_groups = df.groupby(specs.col_group)
    # Drop ticker
    df.drop(specs.col_group,axis=1,inplace=True)
    # Drop date
    df.drop(specs.col_date,axis=1,inplace=True)
    
    # Aggregate data and separate labels
    # + clean the data somewhat
    dataset = aggregate_year(data_groups, specs.col_label, specs.chunk, analyze=specs.analyze)
    
    return dataset

def aggregate_year(data_groups, col_label, chunk, analyze=False):
    dataset = {}
    for group_name, df_group in data_groups:
        # Get basic stats about missing features
        if analyze:
            analyze_missing_features_df(group_name, df_group)
        # Separate revenue
        revenue = df_group[col_label].copy()
        dfg = df_group.drop(col_label,axis=1)
        # prepare to regroup
        nrows, ncols = dfg.shape
        nsteps, row_size = int((nrows-1)/chunk), chunk*ncols
        # Get labels
        labels = np.hstack((revenue.iloc[0],revenue.iloc[4::4]))
        # Get data
        data = np.empty(shape=[0, row_size])
        for i in range(nsteps):
            row_from, row_to = 1+chunk*i,chunk*(i+1)
            step_mtx = dfg.iloc[row_from:row_to+1]
            step_vec = step_mtx.values.reshape(1,row_size)
            data = np.append(data,step_vec,axis=0)
        #print(labels, labels.shape, data.shape)
        # Clean data
        data_cleaned = clean_the_data(group_name, data)
        dataset[group_name] = (data_cleaned, labels)
    return dataset

def clean_the_data(name, data):
    print("\nCleaning ticker {} of size {}".format(name, data.shape))
    # Drop empty columns
    clean_data = data[:, ~np.isnan(data).all(axis=0)]
    bad_num = data.shape[1]-clean_data.shape[1]
    print("{} empty colums deleted!".format(bad_num))
    # set threshold for corrupt column/row
    nr, nc = clean_data.shape
    threshold = (nc // 3, nr // 3)
    bad_cols, bad_rows = analyze_missing_features_na(name, clean_data, threshold)
    # drop hopeless columns
    cleaner_data = np.delete(clean_data, bad_cols, 1)
    bad_num = clean_data.shape[1]-cleaner_data.shape[1]
    print("{} corrupt colums deleted!".format(bad_num))
    return cleaner_data

def analyze_missing_features_na(name, data, threshold):
    """Get stats for numpy array"""
    mask = np.isnan(data)
    rows, cols = mask.sum(1), mask.sum(0)
    miss_col = np.nonzero(cols)
    miss_row = np.nonzero(rows)
    thr_row, thr_col = threshold
    bad_cols = [c for c in np.nditer(miss_col) if cols[c] > thr_col]
    bad_rows = [r for r in np.nditer(miss_row) if rows[r] > thr_row]
    return (bad_cols, bad_rows)

def analyze_missing_features_df(name, df):
    """Get stats about each feature"""
    report = zip(df.columns, df.isnull().sum())
    print("Ticker: ", name)
    print("Feature/Missing:")
    for col, val in report:
        if val == 0: continue
        stmt = "\t{:40} {}".format(col,val)
        print(stmt)
