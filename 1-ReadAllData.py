#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np


# # Reading the data files

# In[2]:


data_path = 'data/'
all_data = []

for folder in listdir(data_path):
    for file in listdir(data_path + folder):
        file_path = data_path + folder + '/' + file
        df = pd.read_csv(file_path)
        df['Gateway'] = folder
        df['Distance'] = file #.replace('m.csv','')
        all_data.append(df)
        
df = pd.concat(all_data)
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Distance'] = pd.to_numeric(df['Distance'])
df = df.sort_values(by = 'DateTime')


# # Filtering unknown tags
# There may some unknow BLE devices which have been detected by our gateways and we should filter them.
# Also, we have 2 data points for each tag: RSSI (Type=1) and TxPower (Type=2)

# In[3]:


df_tag_summary = df.groupby(['TagUid']).count()
df_tag_summary = df_tag_summary['Gateway'].sort_values(ascending=False)
df_tag_summary[:10]


# In[4]:


valid_tags = ['AC:23:3F:25:C0:4D', 'AC:23:3F:25:C7:72', 'AC:23:3F:25:D2:99', 
              'AC:23:3F:25:C7:8C', 'D0:03:4E:14:C0:D3', 'DE:AC:1A:CD:42:BD']
data = df[df['TagUid'].isin(valid_tags)]


# # Filtering for known gateways

# In[5]:


valid_gateways = ['BlueCats', 'Ingics', 'JAALEE', 'MiNew']
data = data[data['Gateway'].isin(valid_gateways)]


# # Changing 9.9m to 10.0m 

# In[6]:


data.drop(['EndpointId', 'tick'], axis = 1, inplace = True)
data.columns = ['TagUid', 'RSSI', 'TxPower', 'DateTime', 'Gateway', 'Distance']
data = data.drop_duplicates()
data['Distance'] = data['Distance'].apply(lambda x: 10.0 if x == 9.9 else x)
#data['Distance'] = data['Distance'].apply(lambda x: 0.03 if x == 0.0 else x)


# # Saving data in a file

# In[7]:


data.to_csv('data.csv', index = False, header = data.columns)

