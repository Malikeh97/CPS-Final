#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns

# read csv file
data = pd.read_csv('data.csv')


# # Selecting a tag, gateway, and TxPower to work on
# 

# In[2]:


TAG = 'AC:23:3F:25:D2:99'
GATEWAY = 'BlueCats'
TX = -44
df = data[(data['TagUid'] == TAG) & (data['Gateway'] == GATEWAY) & (data['TxPower'] == TX)]
df = df.sort_values('DateTime')
df = df.reset_index()
df = df[['Distance', 'DateTime', 'RSSI']]


# # Outlier Function

# In[3]:


def reject_outliers(x, threshold =2):
    std = np.std(x)
    mean = np.mean(x)
    return x[abs(x - mean) < threshold * std]


# # Filtering outliers for different thresholds

# In[4]:


thresholds = np.arange(1,4)
for threshold in thresholds:
    column_name = 'outlier' + str(threshold)
    df[column_name] = np.nan
    
    for dist in df['Distance'].unique():
        x = df[df['Distance'] == dist]['RSSI']
        denoised = reject_outliers(x, threshold)
        df.loc[(df['Distance'] == dist) & df['RSSI'].isin(denoised), column_name] = denoised.values


# # Evaluating and selecting threshold

# In[5]:


dfrssi = pd.melt(df, id_vars=['Distance', 'DateTime'], var_name='Type', value_name='Value')
df1 = pd.melt(df[df['outlier1'].notnull()], id_vars=['Distance', 'DateTime'], var_name='Type', value_name='Value')
df2 = pd.melt(df[df['outlier2'].notnull()], id_vars=['Distance', 'DateTime'], var_name='Type', value_name='Value')
df3 = pd.melt(df[df['outlier3'].notnull()], id_vars=['Distance', 'DateTime'], var_name='Type', value_name='Value')
df_view = pd.concat([dfrssi, df1, df2, df3])

fig, ax = plt.subplots(figsize=(16,8))
sns.boxplot(ax=ax, x = 'Distance', y = 'Value', hue = 'Type', data = df_view)
sns.despine(offset=10, trim=True)


# # Outlier selection with threshold = 2 is the best or not?!

# In[6]:


for distance in df['Distance'].unique():
    plt.figure(figsize=(16,8))
    plt.title('Tag: ' + TAG + ' Gateway: ' + GATEWAY + ' TxPower: ' + str(TX) + 'dBm distance: ' + str(distance) )
    df_view = df[df['Distance'] == distance]
    ax = df_view['RSSI'].plot(label = 'RSSI')
    
    for threshold in [2]: #thresholds:
        column_name = 'outlier' + str(threshold)
        ax = df_view[df_view[column_name].notnull()][column_name].plot(label = 'th=' + str(threshold))
        
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show() 


# # 3 is very high and 1 is too low, so 2 is the best!

# In[7]:


df = df[df['outlier2'].notnull()][['Distance', 'DateTime', 'outlier2']]
df.columns = ['Distance', 'DateTime', 'RSSI']


# # Saving data in a file

# In[8]:


df.to_csv('data_spikes_removed.csv', index = False, header = df.columns)

