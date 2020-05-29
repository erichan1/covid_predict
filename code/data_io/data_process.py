import pandas as pd
import numpy as np
import git


'''
Each section denotes code to work with a specific data set. 
'''

# ==============================================================================
# NYT data US Counties
def import_nytuscounties_data():
    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    datadir = f"{homedir}/data/us/"
    df = pd.read_csv(datadir + 'nyt_us_counties.csv')
    df['date_processed'] = pd.to_datetime(df['date'].values) # add col to represent days from start.
    df['date_processed'] = (df['date_processed'] - df['date_processed'].min()) / np.timedelta64(1, 'D')
    return df

# Select nyt data rows for a specific us county. Only include rows w/ cumulative deaths above min_death. 
def select_county_nytus(df, fips_code, min_deaths=20):
    d = df.loc[df['fips'] == fips_code] # county
    over_mindeath = np.where(d['deaths'].values > min_deaths)[0] # indices
    if(len(over_mindeath) > 0):
        start = np.where(d['deaths'].values > min_deaths)[0][0] # deceased/deaths
        d = d[start:]
    else:
        d = d[len(d):] # empty dataframe
    return d
# ==============================================================================
# Import array of county FIPS keys. fips keys are unique numerical codes for counties.
# returns np array of sorted fips keys.
def import_us_fipskeys():
    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    datadir = f"{homedir}/data/us/"
    df = pd.read_csv(datadir + 'fips_key.csv', encoding='latin-1')
    fips = df['FIPS'].unique()
    fips.sort()
    return fips

# ==============================================================================
# Import Google Mobility data
def import_google_mobility():
    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    datadir = f"{homedir}/data/international/google_mobility/"
    df = pd.read_csv(datadir + 'Global_Mobility_Report.csv')
    df['date_processed'] = pd.to_datetime(df['date'].values)
    df['date_processed'] = (df['date_processed'] - df['date_processed'].min()) / np.timedelta64(1, 'D')
    return df


def select_region_google_mobility(
    df, code=None, sub_1=None, sub_2=None):
    '''
    Takes a subset of the rows of mobility dataset 
    Args:
    df = google_mobility dataframe or a subset of it
    code = country_region_code. find a specific country
    sub_1 = sub_region_1. find a sub region 1 eg California
    sub_2 = sub_region_2. find a sub region 2 eg Los Angeles County in California
    
    note - if any args are given string 'nan', then only rows at a higher geographical level are shown.
    For example, if you wanted to just see data for the entire US, you can do 
    select_region_google_mobility(df, code='nan'). If code was not nan, you'd see lower geographical level data at the 
    state level as well. This makes more sense after you look at the mobility dataset.
    '''
    def isNan(item):
        if(isinstance(item, int) or isinstance(item, float)):
            if(np.isnan(item)):
                return True
        elif(item == 'nan'):
            return True
        return False

    if(isNan(code)):
        df = df.loc[df['country_region_code'].isnull()]
    elif(code != None):
        df = df.loc[df['country_region_code'] == code] 

    if(isNan(sub_1)):
        df = df.loc[df['sub_region_1'].isnull()]
    elif(sub_1 != None):
        df = df.loc[df['sub_region_1'] == sub_1]

    if(isNan(sub_2)):
        df = df.loc[df['sub_region_2'].isnull()]
    elif(sub_2 != None):
        df = df.loc[df['sub_region_2'] == sub_2]

    
    return df


