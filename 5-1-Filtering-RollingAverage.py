#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv file
df = pd.read_csv('data_spikes_removed.csv')


# # Applying filters
window_sizes = np.arange(5, 30, 1)
for window_size in window_sizes:
    column_name = 'Rolling' + str(window_size)
    mean_column_name = 'Mean' + str(window_size)
    df[column_name] = np.nan
    df[mean_column_name] = np.nan

    for dist in df['distance'].unique():
        df.loc[df['distance'] == dist, column_name] =  df[df['distance'] == dist]['rssi'].rolling(window_size).mean()
        df.loc[df['distance'] == dist, mean_column_name] =  df[df['distance'] == dist][column_name].mean()

df['Mean'] = np.nan
for dist in df['distance'].unique():
    df.loc[df['distance'] == dist, 'Mean'] =  df[df['distance'] == dist]['rssi'].mean()


# # Visualizing the rolling averages
for distance in df['distance'].unique():
    plt.figure(figsize=(16,8))
    plt.title('distance: ' + str(distance) + 'm')

    df_view = df[df['distance'] == distance]
    ax = df_view['rssi'].plot(label = str(distance) + 'm')
    ax = df_view['Mean'].plot(label = 'Mean')

    for window_size in window_sizes:
        column_name = 'Rolling' + str(window_size)
        ax = df_view[column_name].plot(label = 'window size: ' + str(window_size))

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()


# # It is hard to decide, we compare the mean of each rolling average

df_out = df[['Mean']].copy()
for i in window_sizes:
    column_name = 'Mean' + str(i)
    df_out[column_name] = np.nan
    df_out[column_name] = df[column_name].copy()

df_out.plot(figsize=(16,8))
plt.show()


# # Conclusion
# We are assuming that we will get data from the tags at least every second. Therefore, there is no reason to go with window size less than 5 steps.
#
# The chart above shows that there is not much difference between them, so we go with samller size.
#
# #### Window size in rolling average = 10
