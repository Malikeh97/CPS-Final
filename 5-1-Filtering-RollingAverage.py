#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv file
df = pd.read_csv('data_spikes_removed.csv')


# # Applying filters

# In[2]:


window_sizes = np.arange(5, 30, 1)
for window_size in window_sizes:
    column_name = 'Rolling' + str(window_size)
    mean_column_name = 'Mean' + str(window_size)
    df[column_name] = np.nan
    df[mean_column_name] = np.nan
    
    for dist in df['Distance'].unique():
        df.loc[df['Distance'] == dist, column_name] =  df[df['Distance'] == dist]['RSSI'].rolling(window_size).mean()
        df.loc[df['Distance'] == dist, mean_column_name] =  df[df['Distance'] == dist][column_name].mean()

df['Mean'] = np.nan
for dist in df['Distance'].unique():
    df.loc[df['Distance'] == dist, 'Mean'] =  df[df['Distance'] == dist]['RSSI'].mean()


# # Visualizing the rolling averages

# In[3]:


for distance in df['Distance'].unique():
    plt.figure(figsize=(16,8))
    plt.title('Distance: ' + str(distance) + 'm')
    
    df_view = df[df['Distance'] == distance]
    ax = df_view['RSSI'].plot(label = str(distance) + 'm')
    ax = df_view['Mean'].plot(label = 'Mean')
    
    for window_size in window_sizes:
        column_name = 'Rolling' + str(window_size)
        ax = df_view[column_name].plot(label = 'window size: ' + str(window_size))
        
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show() 


# # It is hard to decide, we compare the mean of each rolling average

# In[4]:


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
# #### Window size in rolling average = 5
