#this file contains some helpful functions for the notebook

#counts the number of individual data points in an array
def number_of_entries(my_map : map):
    size = len(my_map) 
    print('Number of data columns: ' + repr(size)) 
    first_value_length = len(my_map[next(iter(my_map))]) #get the length of the first array in the map. We only need the first array as they are all the same size
    total_data_number = first_value_length * size
    print( 'Total number of data entries = '  + repr(size)  + ' columns * ' + repr(first_value_length) + ' files = ' + repr(total_data_number))
    return total_data_number
    

#calculate the mean
def mean(array : list):
    return sum(array)/len(array)

#calculate variance
def variance(array : list):
    my_mean = mean(array)
    return sum((x - my_mean) ** 2 for x in array) / len(array)

#calculate standard deviation
def standard_dev(array : list):
    return variance(array) ** 0.5

#calculate range 
def range(array : list):
    return max(array) - min(array)

#find median value
def median(array : list):
    array.sort() # to find the median first we must sort the list
    size = len(array)
    if size % 2 != 0:   #if the size of the array is odd 
        return array[size//2]   #take the middle element
    else:               #else size is even
        lower_median = array[(size - 1) // 2]  #so we must find the two middle elements
        higher_median = array[size // 2]
        return mean([higher_median, lower_median])  #and calculate the average

#find lower quartile value
def lower_quartile(array : list):
    array.sort()    #first we sort the array 
    size = len(array)
    mid_index = size // 2 #then find the middle index
    if size % 2 != 0:       #if the length of the array is odd 
        lower_half = array[:mid_index + 1]  #we get the array sliced up to mid index + 1. We +1 because indexs start from 0
    else:
        lower_half = array[:mid_index] #if its even we just use the mid index because we rounded down earlier with //2
    return median(lower_half) #then find the median of the lower half of the data 

#find upper quartile value
def upper_quartile(array : list):
    array.sort()#first we sort the array 
    size = len(array)
    mid_index = size // 2#then find the middle index
    if size % 2 != 0:  #if the length of the array is odd 
        upper_half = array[mid_index + 1:] #we get the array sliced mid index + 1 to the end. We +1 because indexs start from 0
    else:
        upper_half = array[mid_index:] #if its even we just use the mid index because we rounded down earlier with //2
    return median(upper_half) #then find the median of the upper half of the data 

#calculate skewness of a list. Near 0 means that the data is normally distributed
def skew(array : list):
    n = len(array)
    my_mean = mean(array)
    std_dev = standard_dev(array)
    skewness = (n * sum(((x - my_mean) / std_dev) ** 3 for x in array)) / ((n - 1) * (n - 2))
    return skewness

#check if a list only contains ints or floats
def is_int_or_float_list(list : list):
    for item in list:
        if isinstance(item, int):
            continue
        elif isinstance(item, float):
            continue
        else:
            return False
    return True

#convert miliseconds to string of minutes and seconds for readibility
def ms_to_minutes_seconds(milliseconds):
    if not isinstance(milliseconds, (int, float)):
        return milliseconds
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return str(repr(int(minutes)) + "m and " + repr(int(seconds)) + "s")

#convert the duration_ms array to minutes and seconds
def convert_ms_array(my_map : map):
    if 'duration_ms' in my_map['Column']:
        index = my_map['Column'].index('duration_ms')
        for key in my_map:
            my_map[key][index] = ms_to_minutes_seconds(my_map[key][index])
        return my_map

# Function to parse a CSV line with support for quoted strings
def parse_csv_line(line):
    result = []
    current_field = []
    inside_quotes = False
    for char in line:
        if char == '"':
            # Toggle the inside_quotes flag when encountering a quote
            inside_quotes = not inside_quotes
        elif char == ',' and not inside_quotes:
            # If we encounter a comma and we're not inside quotes, split the field
            result.append(''.join(current_field).strip())
            current_field = []
        else:
            # Add the character to the current field
            current_field.append(char)

    # Append the last field
    result.append(''.join(current_field).strip())
    return result

#load a csv file as a map object 
def load_csv_as_map(file_path):
    my_map = {}
    with open(file_path, 'r', encoding='utf-8') as file:    # Open the CSV file
        lines = file.readlines()
        header = lines[0].strip().split(',')        # First line becomes the keys of the dictionary
        for key in header:
            my_map[key] = []         # Initialize each key in the dictionary with an empty list
        for line in lines[1:]:         # Iterate over the remaining rows
            values = parse_csv_line(line.strip())             # Split the row into values
            for i, key in enumerate(header):             # For each value, try to convert it to int, float 
                value = values[i]
                try:
                    if '.' in value or 'e-' in value:    
                        value = float(value) 
                    else:
                        value = int(value)
                except ValueError:
                    pass
                        
                my_map[key].append(value)

    return my_map

#similar to the pandas own describe() function but I've added variance and range
def descriptive_stats(df : map):
    stat_map = { 'Column' : [], 'Mean' : [], 'Standard deviation' : [], 'Variance' : [], 'Min' : [], 'Max' : [], 'Range' : [], 'Lower Quartile' : [], 'Median' : [], 'Upper Quartile' : [], 'Skewness' : []}
    for key, value in df.items():
        if key == '' or key == 'Unnamed: 0':
            continue #this is used to skip calculating values for the index row as it is pointless to perform calculations on it.
        if is_int_or_float_list(value): #also ensure the columns we are performing calculations on only contain numerical values
            stat_map['Column'].append(key)
            stat_map['Mean'].append(mean(value))
            stat_map['Standard deviation'].append(standard_dev(value))
            stat_map['Variance'].append(variance(value))
            stat_map['Min'].append(min(value))
            stat_map['Max'].append(max(value))
            stat_map['Range'].append(range(value))
            stat_map['Lower Quartile'].append(lower_quartile(value))
            stat_map['Median'].append(median(value))
            stat_map['Upper Quartile'].append(upper_quartile(value)),
            stat_map['Skewness'].append(skew(value))
            
    return stat_map