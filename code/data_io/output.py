from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import git

def import_us_fipskeys():
    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    datadir = f"{homedir}/data/us/"
    df = pd.read_csv(datadir + 'fips_key.csv', encoding='latin-1')
    fips = df['FIPS'].unique()
    fips.sort()
    return fips

# create list of date-fips ids for this county, given list of dates and county code.
def gen_county_ids(dates, fips_key):
    county_ids = []
    for i in range(len(dates)):
        date = dates[i]
        id_ = date.strftime("%Y-%m-%d-") + str(fips_key)
        county_ids.append(id_)
    return county_ids 

# Takes diff of 2D matrix of cumulative deaths to get predicted daily deaths
def cumulative_to_daily(cumulative_deaths):
    daily = np.diff(cumulative_deaths, axis=0)
    daily = np.insert(daily, 0, np.zeros(daily.shape[1]), axis=0)
    return daily

# generates predictions for just one function. test version just to make sure submission format correct.
def test_generate_predictions(predict_func):
    '''
    args: 
    predict_func_dict fips_code: function to predict deaths.
        f(t_eval) -> 2d matrix of dim ((len(t_eval)) x 9 quantiles)
        predict_func must return matrix of deaths for each date, at each quantile.
    todo: account for how functions are trained. april 1 might not match to t=0 in model. 

    rvalue:

    '''
    # Fips Keys
    fips_keys_df = data_process.import_us_fipskeys()
    fips_keys_lst = fips_keys_df['FIPS'].values
    # Fips keys here are not unique - make unique
    fips_keys_lst = np.unique(fips_keys_lst)

    # Dates and Times
    start_date = date(2020,4,1) # Start at April 1st 2020
    end_date = date(2020,6,30) # end at June 30th
    t_eval = [] # times to evaluate by predict_func
    dates = []

    delta = end_date - start_date # total number of days
    for i in range(delta.days + 1):
        dates.append(start_date + timedelta(days=i))
        t_eval.append(i)

    # use lst for fast appending
    quantile_pred_lst = [] 
    id_lst = []
    for fips_key in fips_keys_lst:
        county_output_rows = predict_func(t_eval) # list (len(t_eval) x 9 quantiles) 
        quantile_pred_lst.extend(county_output_rows)
        id_rows = gen_county_ids(dates, fips_key)
        id_lst.extend(id_rows)

    # covert list into dataframe. set index
    submission_df = pd.DataFrame(quantile_pred_lst)
    quantiles = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    submission_df.columns = quantiles # todo set 
    submission_df.insert(0, 'id', id_lst) # put ids at 0th pos

    # output csv 
    now = datetime.now()
    now = now.strftime("%m_%d_%H_%M_%S") # mo, day, hour, min, sec

    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    submissionsdir = f"{homedir}/submissions/"
    submission_df.to_csv(submissionsdir + now + '_submission.csv', index=False)

def generate_predictions(predict_func_dict, is_cumulative=True):
    '''
    args: 
    predict_func_dict fips_code: (function to predict deaths, time offset from apr 1)
        f(t_eval) -> 2d matrix of dim ((len(t_eval)) x 9 quantiles)
        predict_func must return matrix of deaths for each date, at each quantile.
        t_offset = start_date - apr 1
    is_cumulative (boolean): is this prediction function predicting cumulative or daily deaths?

    rvalue:

    '''
    # Fips Keys
    fips_keys_lst = import_us_fipskeys()

    # Dates and Times
    start_date = date(2020,4,1) # Start at April 1st 2020
    end_date = date(2020,6,30) # end at June 30th
    t_eval = [] # times to evaluate by predict_func
    dates = []

    delta = end_date - start_date # total number of days
    for i in range(delta.days + 1):
        dates.append(start_date + timedelta(days=i))
        t_eval.append(i)
    t_eval = np.array(t_eval) # needed for np ops

    # use lst for fast appending
    quantile_pred_lst = [] 
    id_lst = []
    for fips_key in fips_keys_lst:
        predict_func, t_offset = predict_func_dict[fips_key]
        county_output_rows = predict_func(t_eval - t_offset) # list (len(t_eval) x 9 quantiles) 
        if(is_cumulative):
            county_output_rows = cumulative_to_daily(county_output_rows)
        quantile_pred_lst.extend(county_output_rows)
        id_rows = gen_county_ids(dates, fips_key)
        id_lst.extend(id_rows)

    # covert list into dataframe. set index
    submission_df = pd.DataFrame(quantile_pred_lst)
    quantiles = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    submission_df.columns = quantiles # todo set 
    submission_df.insert(0, 'id', id_lst) # put ids at 0th pos

    # output csv 
    now = datetime.now()
    now = now.strftime("%m_%d_%H_%M_%S") # mo, day, hour, min, sec

    repo = git.Repo("./", search_parent_directories=True)
    homedir = repo.working_dir
    submissionsdir = f"{homedir}/submissions/"
    submission_df.to_csv(submissionsdir + now + '_submission.csv', index=False)


