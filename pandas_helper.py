import numpy as np
import pandas as pd
import helper as h
#this data frame is a summary of the number of values in each column and their data type
def data_summary(df : pd.DataFrame):
    summarydf = pd.DataFrame(columns=['Column', 'Data type', 'Size', 'Number of unique Values'])

    for loop_count, column in enumerate(df.columns):
        summarydf.loc[loop_count] = [column, df[column].dtype, df[column].size, df[column].nunique()]   #populate the dataframe with data from dataset 
        
    summarydf.set_index('Column', inplace=True)
    
    return summarydf

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
    total_number_entries = df.columns.size * size
    print( 'Total number of data entries = '  + repr(df.columns.size)  + ' columns * ' + repr(df['track_id'].size) + ' files = ' + repr(total_number_entries))
    return total_number_entries

def descriptive_stats_extended(df : pd.DataFrame):
    statsdf = pd.DataFrame(columns=['Column', 'Mean', 'Standard deviation', 'Variance', 'Min', 'Max', 'Range', 'Lower Quartile', 'Median', 'Upper Quartile', 'Skewness'])
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
                                    df[column].quantile(0.75),
                                    df[column].skew()]

    return statsdf

def edit_dataframe(df : pd.DataFrame):
    running = True
    edited_df = df
    edited_statdf = descriptive_stats_extended(df) 
    columns = df.select_dtypes(include=['number']).columns #this variable is to ensure only numerical columns can be selected for the editing the dataset
    selected_column = pd.Series(dtype='object')
    selected_max = 0
    selected_min = 0
    filter_value = 0
    greater_or_less = ""
    editing_notes = ""
    while running:
        if selected_column.empty:
            column_name = input("enter column to filter by " + repr(columns.values))
            
            if " " in column_name:  #if the user added a space after the column they want to filter by we can remove it using split and access the first word in the list 
                column_name = column_name.split()[0]

            if column_name in columns:
                selected_column = edited_statdf[edited_statdf['Column'] == column_name]
                editing_notes += ("Selected data by " + column_name)
            else:
                print("Please enter a valid column name ")
                continue

        if not selected_column.empty:
            selected_max = selected_column['Max'].values[0]
            selected_min = selected_column['Min'].values[0]
            
        if filter_value == 0:
            filter_value = input("please enter the filter value between MIN: " + repr(selected_min) + " and MAX: " + repr(selected_max))
            
        if greater_or_less == "":
            greater_or_less = input("Would you like to select for values greater (g) or less than (l) " + repr(filter_value) + "?")
        
            if greater_or_less == "g" or greater_or_less == "G":
                edited_df = edited_df[edited_df[column_name] >= float(filter_value)]
                editing_notes += (" >= " + filter_value + "\n")
            elif greater_or_less == "l" or greater_or_less == "L":
                edited_df = edited_df[edited_df[selected_column] <= float(filter_value)]
                editing_notes += (" <= " + filter_value + "\n")
            else:
                print("please enter g or l")
                continue

        print(editing_notes)
        
        continue_editing = input("Would you like to continue editing the dataset? y/n")

        if continue_editing == "y":
            selected_column = pd.Series(dtype='object')
            filter_value = 0
            greater_or_less = ""
            edited_statdf = descriptive_stats_extended(edited_df)
            editing_notes = ""
            continue
        elif continue_editing == "n":
            running = False
        else:
            print("Please enter a valid character (y/n)")
            continue
    return edited_df