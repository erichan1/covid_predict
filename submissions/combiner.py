import pandas as pd
from datetime import datetime


# helper func. works together with join to sum quantile cols
def sum_quantile_cols(df):
    # note - outputs some warnings about view vs. copy. prob don't need to worry.
    quantile_names = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    combined_df = df[['id']]
    for quantile in quantile_names:
        quantile_cols = df.filter(regex='^'+quantile)
        combined_df[quantile] = quantile_cols.sum(axis=1)
    return combined_df


def combine_submissions(submission_filenames):
    '''
    Args:
    submission_filenames (np array, list, list-like): 
        List of strings. Each string is a valid filename of a submission.csv

    todo - add some way to describe what was combined in new file
    note - change destination folder at bottom. 
    '''
    
    quantile_names = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    N_submissions = len(submission_filenames)
    combined_submission_df = pd.read_csv(submission_filenames[0]) # initialize combined submissions
    # add all other submissions
    for i in range(1, N_submissions):
        sub_df = pd.read_csv(submission_filenames[i])

        combined_submission_df = combined_submission_df.join(sub_df.set_index('id'), on='id', rsuffix='_r', how='inner')
        combined_submission_df = sum_quantile_cols(combined_submission_df)

    # divide by N_submissions
    combined_submission_df[quantile_names] = combined_submission_df[quantile_names] / N_submissions

    N_required_rows = 293293 # hardcoded based on sample submission num rows
    assert(len(combined_submission_df) == N_required_rows) # check that num rows is right  
    
    # define a unique time for this submission
    now = datetime.now()
    now = now.strftime("%m_%d_%H_%M_%S") # mo, day, hour, min, sec

    # output. format right now is: folder/(time)_combined.csv
    combined_submission_df.to_csv('submissions/' + now + '_combined.csv', index=False)

# give this a list of filenames
filenames = ['submissions/05_25_21_30_18_submission.csv', 'submissions/submission_test_SEIRQD_May23_1F.csv']
combine_submissions(filenames)




