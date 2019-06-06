#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns

# read csv file
data = pd.read_csv('data.csv')

TAG = 'd6:fb:b2:5e:83:c5'
GATEWAY = 'RaspberryPi'
df = data[(data['uuid'] == TAG)]
df = df.reset_index()
df = df[['uuid', 'distance', 'rssi']]


def reject_outliers(x, threshold = 2):
    std = np.std(x)
    mean = np.mean(x)
    return x[abs(x - mean) < threshold * std]


# # Filtering outliers for different thresholds

# In[4]:


thresholds = np.arange(1,4)
for threshold in thresholds:
    column_name = 'outlier' + str(threshold)
    df[column_name] = np.nan

    for dist in df['distance'].unique():
        x = df[df['distance'] == dist]['rssi']
        denoised = reject_outliers(x, threshold)
        df.loc[(df['distance'] == dist) & df['rssi'].isin(denoised), column_name] = denoised.values


# # Evaluating and selecting threshold
#convert dataframe from wide format to long format

dfrssi = pd.melt(df, id_vars=['distance'], var_name='Type', value_name='Value')
df1 = pd.melt(df[df['outlier1'].notnull()], id_vars=['distance'], var_name='Type', value_name='Value')
df2 = pd.melt(df[df['outlier2'].notnull()], id_vars=['distance'], var_name='Type', value_name='Value')
df3 = pd.melt(df[df['outlier3'].notnull()], id_vars=['distance'], var_name='Type', value_name='Value')
df_view = pd.concat([dfrssi, df1, df2, df3])

fig, ax = plt.subplots(figsize=(16,8))
sns.boxplot(ax=ax, x = 'distance', y = 'Value', hue = 'Type', data = df_view)
sns.despine(offset=10, trim=True)


# # Outlier selection with threshold = 2 is the best or not?!

for distance in df['distance'].unique():
    plt.figure(figsize=(16,8))
    plt.title('Tag: ' + TAG + ' Gateway: ' + GATEWAY + ' distance: ' + str(distance) )
    df_view = df[df['distance'] == distance]
    ax = df_view['rssi'].plot(label = 'RSSI')

    for threshold in [2]: #thresholds:
        column_name = 'outlier' + str(threshold)
        ax = df_view[df_view[column_name].notnull()][column_name].plot(label = 'th=' + str(threshold))

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

# for distance in df['distance'].unique():
#     plt.figure(figsize=(16,8))
#     plt.title('Tag: ' + TAG + ' Gateway: ' + GATEWAY + ' distance: ' + str(distance) )
#     df_view = df[df['distance'] == distance]
#     ax = df_view['rssi'].plot(label = 'RSSI')
#
#     for threshold in [3]: #thresholds:
#         column_name = 'outlier' + str(threshold)
#         ax = df_view[df_view[column_name].notnull()][column_name].plot(label = 'th=' + str(threshold))
#
#     plt.legend(loc='upper left')
#     plt.grid(True)
#     plt.show()
#
# for distance in df['distance'].unique():
#     plt.figure(figsize=(16,8))
#     plt.title('Tag: ' + TAG + ' Gateway: ' + GATEWAY + ' distance: ' + str(distance) )
#     df_view = df[df['distance'] == distance]
#     ax = df_view['rssi'].plot(label = 'RSSI')
#
#     for threshold in [1]: #thresholds:
#         column_name = 'outlier' + str(threshold)
#         ax = df_view[df_view[column_name].notnull()][column_name].plot(label = 'th=' + str(threshold))
#
#     plt.legend(loc='upper left')
#     plt.grid(True)
#     plt.show()


# # 3 is very high and 1 is too low, so 2 is the best!

# In[7]:


df = df[df['outlier2'].notnull()][['uuid','distance', 'outlier2']]
df.columns = ['uuid', 'distance', 'rssi']


# # Saving data in a file

# In[8]:


df.to_csv('data_spikes_removed.csv', index = False, header = df.columns)
