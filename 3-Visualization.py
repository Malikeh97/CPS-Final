#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# read csv file
data = pd.read_csv('data.csv')


# # Selecting a tag, gateway, and TxPower to work on

# In[3]:


TAG = 'AC:23:3F:25:D2:99'
GATEWAY = 'BlueCats'
TX = -44
df = data[(data['TagUid'] == TAG) & (data['Gateway'] == GATEWAY) & (data['TxPower'] == TX)]
df = df.sort_values('DateTime')
df = df.reset_index()


# # How many data points have been saved?

# In[4]:


df_summary = df.groupby(['Distance']).size()
df_summary.plot(kind='bar', figsize=(16,8), grid = True, title = 'RSSI Count')
plt.show()


# # Visualizing RSSI vs Distance

# In[5]:


pd.options.mode.chained_assignment = None
plt.figure(figsize=(16,8))
plt.title('RSSI plot for Tag: ' + TAG + ' Gateway: ' + GATEWAY + ' TxPower: ' + str(TX) + 'dBm' )

for distance in df['Distance'].unique():
    df_view = df[df['Distance'] == distance]
    ax = df_view['RSSI'].plot(label = str(distance) + 'm')

plt.legend(loc='upper left')
plt.grid(True)
plt.show()


# In[5]:


ax = df[['Distance', 'RSSI']].boxplot(by='Distance', figsize=(16,8))
plt.show()

