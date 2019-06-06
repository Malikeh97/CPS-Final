#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv file
data = pd.read_csv('data.csv')


# # Checking collected data

# ### How many data points were collected by each gateway (only RSSI)?

# In[2]:


df_gateway_summary = data.groupby(['Gateway']).size()#.sort_values(ascending=False)
df_gateway_summary.plot(kind='bar', figsize=(16,8), grid = True, title = 'RSSI Count')
plt.show()


# ### How many data points were collected by each gateway (only RSSI) in each range?

# In[3]:


df_gateway_summary = data.groupby(['Gateway', 'Distance']).count()
df_gateway_summary = df_gateway_summary['RSSI'].unstack()
df_gateway_summary


# In[4]:


df_gateway_summary.plot(kind = 'bar', stacked = True, figsize=(16,8), title='RSSI Count', grid= True)
plt.show()


# In[5]:


df_gateway_summary = data.groupby(['TagUid', 'Gateway', 'Distance', 'TxPower']).count()
df_gateway_summary = df_gateway_summary['RSSI'].unstack()
df_gateway_summary

