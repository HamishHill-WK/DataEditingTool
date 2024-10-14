import numpy as np
import pandas as pd
#this file contains some helpful functions for the notebook

#counts the number of individual data points in an array
def number_of_entries(df):
    size = len(df)
    print('Number of files: ' + repr(size))
    print( 'Total number of data entries = '  + repr(df.columns.size)  + ' columns * ' + repr(df['Unnamed: 0'].size) + ' files = ' + repr(df.columns.size *  df['Unnamed: 0'].size))
    print( 'Total number of data entries (excluding index) = ' + repr(df.columns.size - 1)  + ' * ' + repr(df['Unnamed: 0'].size) + ' = ' + repr((df.columns.size - 1) * df['Unnamed: 0'].size))

#calculate the mean
def mean(array):
    return sum(array)/len(array)

#calculate variance
def variance(array):
    this_mean = mean(array)
    return sum((x - this_mean) ** 2 for x in array) / len(array)

#calculate standard deviation
def standard_dev(array):
    return variance(array) ** 0.5

def range(array):
    return max(array) - min(array)

def median(array):
    #print(array)
    array.sort() # to find the median first we must sort the list
    #print(repr(array) + " ") 
    size = len(array)
    #print(size //2)
    if size % 2 != 0:   #if the size of the array is odd 
        print(array[size//2])
        return array[size//2]   #take the middle element
    else:               #else it is even
        lower_median = array[(size - 1) // 2]  #so we must find the two middle elements
        higher_median = array[size // 2]
        #print(mean([higher_median, lower_median]))
        return mean([higher_median, lower_median])  #and calculate the average
    
def lower_quartile(array):
    array.sort()
    size = len(array)
    mid_index = size //2
    if size % 2 != 0:
        lower_half = array[:mid_index + 1]
    else:
        lower_half = array[:mid_index]
    return median(lower_half)

def upper_quartile(array):
    array.sort()
    size = len(array)
    mid_index = size //2
    if size % 2 != 0:
        upper_half = array[mid_index + 1:]
    else:
        upper_half = array[mid_index:]
    return median(upper_half)

#function to check if a variable is a numpy float or int
def is_int_or_float(number):
    return isinstance(number, (np.integer, np.floating))

def is_int_or_float_list(list):
    for item in list:
        #print(repr(type(item)) + " " + item)
        if isinstance(item, int):
            continue
        elif isinstance(item, float):
            continue
        else:
            #print("false :" + repr(item))
            return False
    return True

#convert miliseconds to string of minutes and seconds for readibility
def ms_to_minutes_seconds(milliseconds):
    if not is_int_or_float(milliseconds):
        return milliseconds
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return str(repr(int(minutes)) + "m and " + repr(int(seconds)) + "s")

#This data frame will contain descriptive statistics includes variance and range about the data
#similar to the pandas own describe().transpose()function but I've added variance and Range, as well as a special condition to convert the milliseconds column to minutes and seconds
def descriptive_stats_extended(df : map):
    stat_map = { 'Column name' : [], 'Mean' : [], 'Standard deviation' : [], 'Variance' : [], 'Min' : [], 'Max' : [], 'Range' : [], 'Lower Quartile' : [], 'Median' : [], 'Upper Quartile' : []}
    for key, value in df.items():
        #print(value[1:])
        if key == '':
            continue #this is used to skip calculating values for the index row as it is pointless to perform calculations on it.
        #print(is_int_or_float_list(value))
        if is_int_or_float_list(value): #also ensure the columns we are performing calculations on only contain numerical values
            stat_map['Column name'].append(key)
            stat_map['Mean'].append(mean(value))
            stat_map['Standard deviation'].append(standard_dev(value))
            stat_map['Variance'].append(variance(value))
            stat_map['Min'].append(min(value))
            stat_map['Max'].append(max(value))
            stat_map['Range'].append(range(value))
            stat_map['Lower Quartile'].append(lower_quartile(value))
            stat_map['Median'].append(median(value))
            stat_map['Upper Quartile'].append(upper_quartile(value))
            
            #if key == 'duration_ms': #add a minutes and seconds column after the duration in miliseconds column to improve readibility of song times
            #    statsdf.loc[loop_count + 1] = statsdf.loc[loop_count].apply(ms_to_minutes_seconds)
             #   statsdf.loc[loop_count + 1, 'Column'] = 'duration minutes and seconds'

    return stat_map

def descriptive_stats_extended_pandas(df : pd.DataFrame):
    statsdf = pd.DataFrame(columns=['Column', 'Mean', 'Standard deviation', 'Variance', 'Min', 'Max', 'Range', 'Lower Quartile', 'Median', 'Upper Quartile'])
    for loop_count, column in enumerate(df.columns):
        if loop_count == 0:
            continue #this is used to skip calculating values for the index row as it is pointless to perform calculations on it.
        
        if df[column].dtype == np.int64 or df[column].dtype == np.float64: #also ensure the columns we are performing calculations on only contain numerical values
            statsdf.loc[loop_count] = [column,
                                    mean(df[column]),
                                    standard_dev(df[column]),
                                    variance(df[column]),
                                    min(df[column]),
                                    max(df[column]),
                                    range(df[column]),
                                    lower_quartile(df[column]),
                                    median(df[column]),
                                    upper_quartile(df[column])]
            if column == 'duration_ms': #add a minutes and seconds column after the duration in miliseconds column to improve readibility of song times
                statsdf.loc[loop_count + 1] = statsdf.loc[loop_count].apply(ms_to_minutes_seconds)
                statsdf.loc[loop_count + 1, 'Column'] = 'duration minutes and seconds'

    #statsdf.set_index('Column', inplace=True)
    return statsdf
