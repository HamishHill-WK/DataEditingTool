import numpy as np
import pandas as pd
#this file contains some helpful functions for the notebook

#counts the number of individual data points in a dataframe
def number_of_entries(df : pd.DataFrame):
    print('Number of files: ' + repr(len(df)))
    print( 'Total number of data entries = '  + repr(df.columns.size)  + ' columns * ' + repr(df['Unnamed: 0'].size) + ' files = ' + repr(df.columns.size *  df['Unnamed: 0'].size))
    print( 'Total number of data entries (excluding index) = ' + repr(df.columns.size - 1)  + ' * ' + repr(df['Unnamed: 0'].size) + ' = ' + repr((df.columns.size - 1) * df['Unnamed: 0'].size))

#calculate the mean
def mean(array):
    return sum(array)/len(array)

#function to check if a variable is a numpy float or int
def is_int_or_float(number):
    return isinstance(number, (np.integer, np.floating))

#convert miliseconds to string of minutes and seconds
def ms_to_minutes_seconds(milliseconds):
    if not is_int_or_float(milliseconds):
        return milliseconds
    total_seconds = milliseconds // 1000  
    minutes = total_seconds // 60         
    seconds = total_seconds % 60          
    return str(repr(int(minutes)) + "m and " + repr(int(seconds)) + "s")

#This data frame will contain descriptive statistics includes variance and range about the data
#similar to the pandas own describe().transpose()function but I've added variance and Range, as well as a special condition to convert the milliseconds column to minutes and seconds
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

    #statsdf.set_index('Column', inplace=True)
    return statsdf

