# Hamish Hill 

## Data Visualisation tool 

## Goal

The goal of this application was to extract descriptive statistics about popular music on the
spotify platform. Using descriptive statistics is useful as it allows us to condense a large
collection of data into interpretable figures, without looking at every single individual data
point. Some of these figures like median or skew allow us to gain insights into the "shape" of
the data. This enables us to investigate the attributes of the most popular songs on the
platform, which could be used to create a model to predict the success of a song. It can also
be used to identify current trends or give insights into what the average song on the platform
is like. Additionally to compare the popularity of different artists and different genres.

## Dataset

The data set used was the Spotify Tracks Dataset (www.kaggle.com, n.d.), which contains
114,000 songs from 125 different genres. Each song has 20 columns of data associated with
it, bringing the total number of data points in the set to 2,280,000 (114,000 * 20). The 20 data
points for each song in the dataset are track_id, artists, album_name, track_name, popularity,
duration_ms, explicit, danceability, energy, key, loudness, mode, speechiness, acousticness,
instrumentalness, liveness, valence, tempo, time_signature and track_genre. Definitions for
these terms have not been included in this report for the sake of brevity, they can be found in
the readme with the project files or on the webpage for the dataset.

## Methods

### helper.py

This python file contains all of the function definitions for the application that don't use
pandas or numpy. It was decided to put all the function definitions into a file so that all the
functions used could be defined when the file is imported as a module and to keep the main
notebook clean. The following functions below are defined in this file.

#### def load_csv_as_map(df : map):

I wrote a function to load in the dataset as a map object which used the first row of the csv
file, which contained the names of the columns of data, to make the keys. Then assigned all
the data within each column to an array for each key. The function will also attempt to
convert all float and integer values as appropriate.

#### def parse_csv_line(line):

This function helps to process the strings from the csv file when loading them to the map
object in the load_csv_as_map function. This was necessary as some of the names in the csv
contain commas.

#### def mean(array : list):

Simple mean calculation function. It returns the sum of the values of the list divided by the
length of the list. This is the average value of the dataset, providing a measure of central
tendency.

#### def variance(array : list):

This function calculates the variance of the values in a given array. Variance represents how
much the data varies from the mean. It provides a sense of the overall dispersion in the data.

#### def standard_dev(array : list):

This function calculates the standard deviation of the values in a given array. Standard
deviation shows the spread of data around the mean.

#### def range(array : list):

This function returns the difference between the minimum and maximum values in an array.

#### def median(array : list):

This function returns the middle value of the array after it has been sorted. This provides an
alternative to the mean for assessing central tendency, although it is not affected by outliers.

#### def lower_quartile(array : list):

This function returns the value which is halfway between the start of the array and the median
of the array.

#### def upper_quartile(array : list):

This function returns the value which is halfway between the median of the array and the end
of the array.

#### def skew(array : list):

This function calculates the true tendency of the data relative to the mean. Skewness of 0
indicates that the data is normally distributed, the spread of values is symmetrical on either
side of the mean. A negative skew indicates that the data has a longer left tail and a positive
skew indicates that the data has a longer right tail. (university.gooddata.com, n.d.)

#### def is_int_or_float_list(list : list):

This function determines if the array only contains int or float values. This is used in the
descriptive_stats function to avoid errors which would occur if non-numerical values were
passed into one of the above functions (mean etc.) which rely on the array only containing
numerical values.

#### def ms_to_minutes_seconds(milliseconds):

This function converts a value in milliseconds to minutes and seconds. This is useful for
improving readability for the user.

#### def convert_ms_array(my_map : map):

This function takes a map object and converts the values stored with the duration_ms key
from milliseconds into minutes and seconds.

#### def descriptive_stats(df : map):

This function returns a map containing the following keys which each have an array of values
associated with them: Column, Mean, Standard deviation, Variance, Min, Max, Range, Lower
Quartile, Median, Upper Quartile, Skewness. The column key contains the names of the
categories from the original dataset.

#### def number_of_entries(my_map : map):

This function returns the total number of files in the map. This is useful for ensuring that the
data has been loaded correctly.

### dash_helper.py

This file is separate from the helper.py file and contains the function which handles the Dash
application for visualising data. Visualising data can help users to understand a dataset. The
interactivity enables the user to easily manipulate the graphical output. The compare_axes
function returns the layout for the dash application.

### pandas_helper.py

This file is separate from the helper.py file and contains some functions which use pandas.
The descriptive_stats_extended and number_of_entries functions in this file have the same
purpose as the functions described in the other helper.py file however they make use of
pandas and numpy language features.

#### def edit_dataframe(df : pd.DataFrame):

This allows the user to make a new dataset by selecting for numerical values in the data. It
returns the dataset once editing is complete.

#### def data_summary(df : pd.DataFrame):

This function returns a dataframe which contains the data type of each column in the data
frame and the number of unique values in that column.

## Evaluation

The application provides some basic descriptive statistics about the data set, which are useful
for gaining insights about the data. The application also provides functionality which enables
the user to create new datasets within stated parameters, this enables the user to gain insights
into specific portions of the dataset. The skewness calculation as well as variance and
standard deviation enable the user to determine if the data is normally distributed.

Some of the calculation functions I've written have slightly different results to the equivalent
pandas functions. The standard deviation and variance function are different. The difference
is insignificant for this exercise, however, the functions would not be suitable for tasks which
require extreme levels of precision such as examining data from particle physics experiments.

### Figure 1) Standard deviation calculations

| Category | My function result | Pandas function result | Difference |
|----------|-------------------|------------------------|------------|
| popularity | 22.30498 | 22.30508 | 9.7E-05 |
| duration_ms | 107297.2 | 107297.7 | 0.470605 |
| danceability | 0.173541 | 0.173542 | 1E-06 |
| energy | 0.251528 | 0.251529 | 1E-06 |
| key | 3.559972 | 3.559987 | 1.5E-05 |
| loudness | 5.029315 | 5.029337 | 2.2E-05 |
| mode | 0.480707 | 0.480709 | 2E-06 |
| speechiness | 0.105732 | 0.105732 | 0 |
| acousticness | 0.332521 | 0.332523 | 2E-06 |
| instrumentalness | 0.309553 | 0.309555 | 2E-06 |
| liveness | 0.190377 | 0.190378 | 1E-06 |
| valence | 0.25926 | 0.259261 | 1E-06 |
| tempo | 29.97807 | 29.9782 | 0.000132 |
| time_signature | 0.432619 | 0.432621 | 2E-06 |

### Figure 2) Variance calculations

| Category | My function result | Pandas function result | Difference |
|----------|-------------------|------------------------|------------|
| popularity | 4.98E+02 | 4.98E+02 | 4.30E-03 |
| duration_ms | 1.15E+10 | 1.15E+10 | 100000 |
| danceability | 3.01E-02 | 3.01E-02 | 2.7E-07 |
| energy | 6.33E-02 | 6.33E-02 | 5.5E-07 |
| key | 1.27E+01 | 1.27E+01 | 0.00011 |
| loudness | 2.53E+01 | 2.53E+01 | 0.00022 |
| mode | 2.31E-01 | 2.31E-01 | 2E-06 |
| speechiness | 1.12E-02 | 1.12E-02 | 1E-07 |
| acousticness | 1.11E-01 | 1.11E-01 | 9E-07 |
| instrumentalness | 9.58E-02 | 9.58E-02 | 8.4E-07 |
| liveness | 3.62E-02 | 3.62E-02 | 3.2E-07 |
| valence | 6.72E-02 | 6.72E-02 | 5.9E-07 |
| tempo | 8.99E+02 | 8.99E+02 | 0.0079 |
| time_signature | 1.87E-01 | 1.87E-01 | 1.6E-06 |

As the variance function is used to calculate the standard deviation, the difference in results
for the standard deviation function could be caused by the differences which are present in
the results of the variance function.

The dash application provides some decent functionality for making a scatter graph with the
data. The ability to select multiple items in each category allows for comparisons between
many items in the data. The ability to adjust the axes also allows the user to examine the data
visually in a variety of different ways. This could be improved by providing functionality for
more kinds of graphs. The regression lines should also be changed to match the colour of the
data they are representing.

The application would benefit from integration of ANOVA and/ or t-test functionality in
order to test the statistical significance of the difference between the data points. The
integration of non-parametric test functions would also be beneficial for when the data is not
normally distributed.

The application is quite limited in its usefulness as it only provides the user the ability to look
at general descriptive statistics and edit the dataset. Further statistical functionality would
make it much more useful. It is difficult to get any meaningful insights into the data without
ANOVAs or t-tests or other non-parametric tests which could determine statistical
significance.

A limitation of the dataset is that there is no mention of when the data was captured either
within the dataset or on the webpage it is hosted on. The explanation for the popularity
variable mentions that the recency of plays is a factor in the calculation but without any
reference to when the data was captured it is difficult to determine when this data will
become outdated.

## References

www.kaggle.com. (n.d.). Spotify Tracks Dataset. [online] Available at:
https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data.

university.gooddata.com. (n.d.). Normality Testing - Skewness and Kurtosis. [online]
Available at:
https://university.gooddata.com/tutorials/creating-metrics/normality-testing-skewness-and-kurtosis/.
