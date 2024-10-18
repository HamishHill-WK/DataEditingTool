import numpy as np
import pandas as pd

#convert miliseconds to string of minutes and seconds for readibility
def ms_to_minutes_seconds(milliseconds):
    if not isinstance(milliseconds, np.number):
        return milliseconds
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return str(repr(int(minutes)) + "m and " + repr(int(seconds)) + "s")

def number_of_entries(df : pd.DataFrame):
    size = len(df)
    print('Number of files: ' + repr(size))
    print( 'Total number of data entries = '  + repr(df.columns.size)  + ' columns * ' + repr(df['Unnamed: 0'].size) + ' files = ' + repr(df.columns.size *  df['Unnamed: 0'].size))

def descriptive_stats_extended(df : pd.DataFrame):
    statsdf = pd.DataFrame(columns=['Column', 'Mean', 'Standard deviation', 'Variance', 'Min', 'Max', 'Range', 'Lower Quartile', 'Median', 'Upper Quartile'])

    for loop_count, column in enumerate(df.columns):
        if loop_count == 0:
            continue #this is used to skip calculating values for the index row as it is pointless to perform calculations on it.
        
        if df[column].dtype == np.int64 or df[column].dtype == np.float64: #also ensure the columns we are performing calculations on only contain numerical values
            statsdf.loc[loop_count] = [column,
                                    df[column].mean(),
                                    df[column].std(),
                                    df[column].var(),
                                    df[column].min(),
                                    df[column].max(),
                                    np.ptp(df[column]),
                                    df[column].quantile(0.25),
                                    df[column].median(),
                                    df[column].quantile(0.75)]
            if column == 'duration_ms': #add a minutes and seconds column after the duration in miliseconds column to improve readibility of song times
                statsdf.loc[loop_count + 1] = statsdf.loc[loop_count].apply(ms_to_minutes_seconds)
                statsdf.loc[loop_count + 1, 'Column'] = 'duration minutes and seconds'

    return statsdf